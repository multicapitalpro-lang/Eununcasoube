"""Gera narração (Kokoro pf_dora, pt-BR feminina), trilha e efeitos sonoros do Vídeo 01.
Uso: python3 -I build_audio.py <pasta_modelo_kokoro> <pasta_saida>
Saída: vo.wav, mix.wav (voz+trilha+sfx) e times.json (início/fim de cada fala)."""
import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
M, OUT = sys.argv[1], sys.argv[2]
SPEC = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "-" else None
VOICE = sys.argv[4] if len(sys.argv) > 4 else None  # pasta com 0.wav, 1.wav... (ex.: Chatterbox)
SR = 24000
LINES = [
 "Você provavelmente está usando seu celular de um jeito que pode estar acabando com a bateria mais rápido.",
 "Baterias de lítio não gostam de ficar constantemente em extremos, principalmente totalmente descarregadas, ou passando muito tempo em condições de calor.",
 "E tem um detalhe ainda mais importante: o calor acelera o desgaste da bateria.",
 "Por isso, deixar o celular carregando em um lugar muito quente, como dentro do carro no sol, pode ser uma péssima ideia.",
 "Agora me diz: você costuma deixar o celular carregando a noite inteira?"]
if SPEC: LINES = json.load(open(SPEC))["lines"]
k = None if VOICE else Kokoro(f"{M}/kokoro-v1.0.onnx", f"{M}/voices-v1.0.bin")
LEAD, GAP, TAIL = 0.35, 0.22, 1.1
segs, times, t = [], [], LEAD
for n_, l in enumerate(LINES):
    if VOICE:
        s, sr = sf.read(f"{VOICE}/{n_}.wav"); s = (s if s.ndim == 1 else s.mean(1)).astype(np.float32)
        assert sr == SR, sr
    else:
        s, sr = k.create(l, voice="pf_dora", speed=1.2, lang="pt-br")
        s = s.astype(np.float32)
    # corta silêncio das pontas
    idx = np.where(np.abs(s) > 0.01)[0]; s = s[idx[0]:idx[-1] + 1]
    times.append([round(t, 3), round(t + len(s) / SR, 3)]); segs.append((t, s)); t += len(s) / SR + GAP
total = round(t - GAP + TAIL, 3)
vo = np.zeros(int(total * SR), np.float32)
for st, s in segs: vo[int(st * SR):int(st * SR) + len(s)] += s
vo /= max(1e-6, np.abs(vo).max()) / 0.9
sf.write(f"{OUT}/vo.wav", vo, SR)
json.dump({"lines": times, "total": total}, open(f"{OUT}/times.json", "w"))

# ---- trilha: pad grave misterioso + pulso suave (sem sidechain, volume constante sob a fala) ----
n = len(vo); tt = np.arange(n) / SR; rng = np.random.default_rng(7)
def tone(f, a): return a * np.sin(2 * np.pi * f * tt + rng.random() * 6.28)
pad = sum(tone(f, a) for f, a in [(55, .5), (82.4, .35), (110, .25), (164.8, .12), (130.8, .1)]) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.12 * tt))
pulse = np.zeros(n)
for b in np.arange(0.0, total, 0.5):  # batida a 120 bpm, grave discreto
    i = int(b * SR); L = int(0.18 * SR)
    if i + L < n: pulse[i:i + L] += np.sin(2 * np.pi * 52 * np.arange(L) / SR) * np.exp(-np.arange(L) / (0.05 * SR)) * 0.5
tick = np.zeros(n)
for b in np.arange(0.25, total, 0.5):
    i = int(b * SR); L = int(0.03 * SR)
    if i + L < n: tick[i:i + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / (0.006 * SR)) * 0.05
music = pad * 0.5 + pulse * 0.6 + tick
env = np.minimum(1, tt / 0.6) * np.minimum(1, (total - tt) / 0.9)
music = music * env; music /= np.abs(music).max()

# ---- efeitos: whoosh nas viradas de cena, toque de UI, estalo no final ----
sfx = np.zeros(n)
def whoosh(at, d=0.5, up=True):
    L = int(d * SR); x = rng.standard_normal(L); w = np.hanning(L) ** 1.5
    # passa-banda varrendo
    from numpy.fft import rfft, irfft
    X = rfft(x); fr = np.fft.rfftfreq(L, 1 / SR)
    c = np.linspace(400, 3500, L).mean() if up else 900
    X *= np.exp(-((np.log(fr + 1) - np.log(c)) ** 2) / 1.2)
    y = irfft(X, L) * w; y /= np.abs(y).max() + 1e-9
    i = int(at * SR); sfx[i:i + L] += y[:max(0, min(L, n - i))] * 0.6 if i + L <= n else 0
def ping(at, f=1760, d=0.35, a=0.35):
    L = int(d * SR); x = np.sin(2 * np.pi * f * np.arange(L) / SR) * np.exp(-np.arange(L) / (0.08 * SR))
    i = int(at * SR)
    if i + L <= n: sfx[i:i + L] += x * a
starts = [0.0] + [times[i][0] - 0.12 for i in (1, 2, 3, 4)]
for s in starts[1:]: whoosh(max(0, s))
ping(0.05, 220, 0.9, 0.5); ping(times[4][1] + 0.1, 1318, 0.6, 0.3); ping(times[4][1] + 0.25, 1760, 0.8, 0.3)
sfx = np.clip(sfx, -1, 1)

mix = vo * 1.0 + music * 0.20 + sfx * 0.30
mix = np.tanh(mix * 1.1)
sf.write(f"{OUT}/mix_raw.wav", mix, SR)
print(json.dumps({"lines": times, "total": total}))
