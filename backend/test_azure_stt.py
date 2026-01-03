import os
import time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("AZURE_SPEECH_KEY")
region = os.getenv("AZURE_SPEECH_REGION")

print(f"Testing Azure STT (Speech-to-Text)...")
if not key:
    print("FATAL: No AZURE_SPEECH_KEY found in .env")
    exit(1)

# Using English explicitly to avoid Auto-Detect complexity
speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
speech_config.speech_recognition_language="en-US"

# Use PushStream to simulate exact conditions
stream = speechsdk.audio.PushAudioInputStream()
audio_config = speechsdk.audio.AudioConfig(stream=stream)

print("Building Recognizer...")
try:
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
except Exception as e:
    print(f"FATAL: Failed to build recognizer: {e}")
    exit(1)

done = False
def stop_cb(evt):
    print(f"SESSION STOPPED: {evt}")
    global done
    done = True

def canceled_cb(evt):
    print(f"\nFATAL CANCELED: Reason={evt.result.reason}")
    print(f"Error Details: {evt.error_details}")

recognizer.recognized.connect(lambda evt: print(f"RECOGNIZED: {evt.result.text}"))
recognizer.recognizing.connect(lambda evt: print(f"PARTIAL: {evt.result.text}"))
recognizer.canceled.connect(canceled_cb)
recognizer.session_stopped.connect(stop_cb)
recognizer.session_started.connect(lambda evt: print(f"SESSION STARTED: {evt}"))

print("Starting Continuous Recognition Async...")
recognizer.start_continuous_recognition_async()

# Send 5 seconds of silence (16kHz * 2 bytes = 32000 bytes/sec)
print("Sending audio silence (5 seconds)...")
try:
    for i in range(10):
        # 3200 bytes = 100ms
        stream.write(bytes([0] * 3200))
        time.sleep(0.1)
        if i % 2 == 0: print(".", end="", flush=True)

    print("\nStopping Recognition...")
    recognizer.stop_continuous_recognition_async()
    # Wait for stop event
    time.sleep(1)

except Exception as e:
    print(f"\nCRASH during loop: {e}")

print("\nDone.")
