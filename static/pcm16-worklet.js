// static/pcm16-worklet.js
class PCM16Worklet extends AudioWorkletProcessor {
  constructor(options) {
    super();
    this.targetRate = options.processorOptions?.targetSampleRate || 16000;
    this.inRate = sampleRate;
    this.carry = new Float32Array(0);
  }

  process(inputs, outputs) {
    const input = inputs[0];
    if (!input || input.length === 0) return true;
    const ch = input[0];
    if (!ch || ch.length === 0) return true;

    let data = ch;
    if (this.carry.length) {
      const tmp = new Float32Array(this.carry.length + ch.length);
      tmp.set(this.carry, 0);
      tmp.set(ch, this.carry.length);
      data = tmp;
      this.carry = new Float32Array(0);
    }

    const ratio = this.inRate / this.targetRate;
    const outLen = Math.floor(data.length / ratio);
    if (outLen === 0) { this.carry = data; return true; }

    const f32 = new Float32Array(outLen);
    let o = 0, i = 0;
    while (o < outLen) {
      const nextI = Math.floor((o + 1) * ratio);
      let sum = 0, count = 0;
      for (; i < nextI && i < data.length; i++, count++) sum += data[i];
      f32[o++] = count ? (sum / count) : 0;
    }

    // DEBUG: Check Amplitude
    let maxAmp = 0;
    for (let i = 0; i < f32.length; i++) {
      const abs = Math.abs(f32[i]);
      if (abs > maxAmp) maxAmp = abs;
    }
    // Log only loud-ish frames to avoid spamming silence, or just log every ~100th
    if (Math.random() < 0.05) {
      this.port.postMessage({ log: `Mic Amp: ${maxAmp.toFixed(3)}` });
    }

    const consumed = Math.floor(outLen * ratio);
    if (consumed < data.length) this.carry = data.slice(consumed);

    // Float32 -> Int16LE
    const buffer = new ArrayBuffer(f32.length * 2);
    const view = new DataView(buffer);
    for (let j = 0; j < f32.length; j++) {
      let s = Math.max(-1, Math.min(1, f32[j]));
      view.setInt16(j * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }

    // BUFFERING: Wait until we have ~4KB (approx 128ms) to reduce socket overhead
    // processing 125 packets/sec is too heavy for SocketIO + Azure SDK.
    if (!this._bytes) this._bytes = [];
    const newBytes = new Uint8Array(buffer);
    for (let b of newBytes) this._bytes.push(b);

    if (this._bytes.length >= 4096) {
      const chunk = new Uint8Array(this._bytes);
      this.port.postMessage({ pcm: chunk.buffer }, [chunk.buffer]);
      this._bytes = [];
    }


    // keep graph alive by zero-filling output (if any)
    const out = outputs[0];
    if (out && out.length) for (let c = 0; c < out.length; c++) out[c].fill(0);
    return true;
  }
}
registerProcessor('pcm16-encoder', PCM16Worklet);
