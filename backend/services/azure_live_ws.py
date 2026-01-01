import os, requests
from flask import request
from flask_socketio import Namespace
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import PushAudioInputStream, AudioConfig, AudioStreamFormat
from azure.cognitiveservices.speech.languageconfig import AutoDetectSourceLanguageConfig

load_dotenv()

def _to_bcp47(lang: str) -> str:
    if not lang: return "en-US"
    if "-" in lang: return lang
    return {
        "en":"en-US","es":"es-ES","fr":"fr-FR","de":"de-DE","it":"it-IT","pt":"pt-PT",
        "hi":"hi-IN","ja":"ja-JP","ko":"ko-KR","zh-Hans":"zh-CN","zh-Hant":"zh-TW",
        "ar":"ar-SA","am":"am-ET"
    }.get(lang, lang)

def _short(lang: str) -> str:
    return (lang or "en").split("-")[0]

def _translate(text: str, src_short: str, tgt_short: str) -> str:
    if not text: return ""
    ep  = (os.getenv("AZURE_TRANSLATOR_ENDPOINT") or "").rstrip("/")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    reg = os.getenv("AZURE_TRANSLATOR_REGION")  # optional depending on your resource
    if not ep or not key: return ""
    try:
        r = requests.post(
            f"{ep}/translate",
            params={"api-version":"3.0","to":tgt_short, "from":src_short},
            headers={
                "Ocp-Apim-Subscription-Key": key,
                "Content-Type": "application/json",
                **({"Ocp-Apim-Subscription-Region": reg} if reg else {})
            },
            json=[{"Text": text}],
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        trs = data[0].get("translations") if isinstance(data, list) and data else None
        return (trs[0].get("text") if trs else "") or ""
    except Exception as e:
        print(f"[azure-live] translate error: {e}")
        return ""

def _detected_bcp47_from(evt):
    try:
        res = speechsdk.AutoDetectSourceLanguageResult.from_result(evt.result)
        return getattr(res, "language", None)
    except Exception:
        return None

class AzureLiveNamespace(Namespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self._streams = {}  # sid -> PushAudioInputStream
        self._recs    = {}  # sid -> SpeechRecognizer
        self._langs   = {}  # sid -> (src_short, tgt_short)
        self._auto    = {}  # sid -> bool

    def on_connect(self, auth):
        sid = request.sid
        auto = False
        if isinstance(auth, dict):
            auto = bool(auth.get("auto_detect", False))
        self._auto[sid] = auto
        print(f"[azure-live] connected {sid} auto={auto}")

    def on_disconnect(self):
        sid = request.sid
        print(f"[azure-live] disconnected {sid}")
        self._stop_session(sid, remove=True)

    def on_set_auto_detect(self, data):
        sid = request.sid
        enabled = bool((data or {}).get("enabled", False))
        self._auto[sid] = enabled
        self.emit("auto_detect_updated", {"enabled": enabled}, room=sid)

    def on_set_langs(self, data):
        sid = request.sid
        if not isinstance(data, dict): return
        src = data.get("src_lang") or "en"
        tgt = data.get("tgt_lang") or "es"
        self._langs[sid] = (_short(src), _short(tgt))
        self.emit("langs_updated", {"src": src, "tgt": tgt}, room=sid)

        # if auto-detect off, restart recognizer in fixed language
        if not self._auto.get(sid, False):
            self._build_and_start_recognizer(sid, _to_bcp47(src), auto_flag=False)

    def on_start_stream(self, data):
        sid = request.sid
        print(f"[azure-live] start_stream {sid} data={data}")
        self._stop_session(sid, remove=True)

        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_reg = os.getenv("AZURE_SPEECH_REGION")
        print(f"[azure-live] keys present? key={'yes' if speech_key else 'no'} region={'yes' if speech_reg else 'no'}")
        
        if not speech_key or not speech_reg:
            print(f"[azure-live] ERROR: missing speech env vars")
            self.emit("error", {"error": "missing_speech_env"}, room=sid)
            return

        src_in = (data or {}).get("src_lang") or "en"
        tgt_in = (data or {}).get("tgt_lang") or "es"
        src_bcp47 = _to_bcp47(src_in)
        self._langs[sid] = (_short(src_bcp47), _short(tgt_in))

        auto_flag = self._auto.get(sid, bool((data or {}).get("auto_detect", False)))
        self._build_and_start_recognizer(sid, src_bcp47, auto_flag=auto_flag)
        self.emit("started", {"ok": True}, room=sid)

    def on_audio_chunk(self, data):
        sid = request.sid
        stream = self._streams.get(sid)
        if not stream:
            # print(f"[azure-live] warning: no stream for {sid}")
            return

        if isinstance(data, dict):
            s = data.get("src_lang")
            t = data.get("tgt_lang")
            if s or t:
                src, tgt = self._langs.get(sid, ("en","es"))
                if s: src = _short(s)
                if t: tgt = _short(t)
                self._langs[sid] = (src, tgt)
            chunk = data.get("chunk")
        else:
            chunk = data

        b = chunk if isinstance(chunk, (bytes, bytearray)) else bytes(chunk or b"")
        if not b:
            return
        
        if len(b) > 0 and (hash(b) % 50 == 0):
             # Check for silence (simple max byte check for activity)
             try:
                 # audioop is removed in Py3.13. Just check if we have non-zero bytes.
                 max_val = max(b)
                 print(f"[azure-live] audio_chunk {sid} len={len(b)} max_byte={max_val}") 
             except Exception as e:
                 print(f"[azure-live] audio_chunk {sid} len={len(b)} log_err={e}") 
        
        try:
            stream.write(b)
        except Exception as e:
            print(f"[azure-live] write error {sid}: {e}")

    def on_end_of_stream(self):
        sid = request.sid
        print(f"[azure-live] end_of_stream {sid}")
        self._stop_session(sid, remove=False)
        self.emit("stopped", {"ok": True}, room=sid)

    # ----- internals -----

    def _attach_handlers(self, rec, sid):
        def _maybe_emit_detected(evt):
            detected = _detected_bcp47_from(evt)
            if detected:
                self.emit("lang_detected", {"detected": detected}, room=sid)
                expected_short = self._langs.get(sid, ("en","es"))[0]
                if _short(detected) and expected_short and _short(detected) != expected_short:
                    self.emit("lang_warning", {"detected": _short(detected)}, room=sid)

        def _on_partial(evt):
            print(f"[azure-live] partial from Azure: {evt.result.text}")
            _maybe_emit_detected(evt)
            txt = evt.result.text or ""
            self.emit("partial_result", {"text": txt}, room=sid)

        def _on_final(evt):
            print(f"[azure-live] FINAL from Azure: {evt.result.text}")
            _maybe_emit_detected(evt)
            txt = evt.result.text or ""
            self.emit("final_result", {"text": txt}, room=sid)

            detected = _detected_bcp47_from(evt)
            src_eff = _short(detected) if detected else self._langs.get(sid, ("en","es"))[0]
            tgt_eff = self._langs.get(sid, ("en","es"))[1]
            tx = _translate(txt, src_eff, tgt_eff)
            if tx:
                self.emit("final_translation", {"translation": tx}, room=sid)

        rec.recognizing.connect(_on_partial)
        rec.recognized.connect(_on_final)
        rec.canceled.connect(lambda evt: print(f"[azure-live] CANCELED: {evt.result.reason} | {evt.error_details}"))
        rec.session_started.connect(lambda evt: print(f"[azure-live] SESSION STARTED {evt}"))
        rec.session_stopped.connect(lambda evt: print(f"[azure-live] SESSION STOPPED {evt}"))

    def _build_and_start_recognizer(self, sid, src_bcp47: str, auto_flag: bool):
        self._stop_session(sid, remove=False)

        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_reg = os.getenv("AZURE_SPEECH_REGION")
        print(f"[azure-live] initializing recognizer for {sid} region={speech_reg}")
        
        speech_cfg = speechsdk.SpeechConfig(subscription=speech_key, region=speech_reg)

        fmt = AudioStreamFormat(samples_per_second=16000, bits_per_sample=16, channels=1)
        stream = PushAudioInputStream(stream_format=fmt)
        audio = AudioConfig(stream=stream)

        if auto_flag:
            detect_langs = list({src_bcp47,"en-US","es-ES","fr-FR","de-DE","it-IT","pt-PT",
                                 "hi-IN","ja-JP","ko-KR","zh-CN","zh-TW","ar-SA","am-ET"})
            auto_cfg = AutoDetectSourceLanguageConfig(languages=detect_langs)
            rec = speechsdk.SpeechRecognizer(
                speech_config=speech_cfg,
                audio_config=audio,
                auto_detect_source_language_config=auto_cfg
            )
        else:
            speech_cfg.speech_recognition_language = src_bcp47
            rec = speechsdk.SpeechRecognizer(speech_config=speech_cfg, audio_config=audio)

        self._attach_handlers(rec, sid)
        self._streams[sid] = stream
        self._recs[sid] = rec

        print(f"[azure-live] starting continuous recognition async...")
        rec.start_continuous_recognition_async().get()
        print(f"[azure-live] started recognition successfully")

    def _stop_session(self, sid, remove=False):
        stream = self._streams.get(sid)
        rec = self._recs.get(sid)
        try:
            if stream: stream.close()
        except Exception:
            pass
        try:
            if rec: rec.stop_continuous_recognition_async().get()
        except Exception:
            pass

        if remove:
            self._streams.pop(sid, None)
            self._recs.pop(sid, None)
            self._langs.pop(sid, None)
            self._auto.pop(sid, None)
