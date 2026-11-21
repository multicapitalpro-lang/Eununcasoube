"""Gera as falas de cada vídeo com o Chatterbox multilingual (clonando a voz de ref.wav).
Uso (no venv do Chatterbox): python gen_voz_chatterbox.py <ref.wav> <saida_dir> spec1.json spec2.json ...
Saída: <saida_dir>/<nome-do-spec>/<i>.wav (24 kHz). Refaz a fala se a duração sair fora do esperado."""
import sys, os, json, time, torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
ref, out = sys.argv[1], sys.argv[2]
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
for sp in sys.argv[3:]:
    name = os.path.basename(sp)[:-5]; os.makedirs(f"{out}/{name}", exist_ok=True)
    for i, t in enumerate(json.load(open(sp))["lines"]):
        p = f"{out}/{name}/{i}.wav"
        if os.path.exists(p): continue
        for tent in range(3):
            torch.manual_seed(100*i + tent)
            t0 = time.time()
            w = m.generate(t, language_id="pt", audio_prompt_path=ref, exaggeration=0.5, cfg_weight=0.5)
            d = w.shape[-1] / m.sr; cps = len(t) / d
            print(f"{name}/{i} tent{tent} {d:.1f}s {cps:.1f} car/s ({time.time()-t0:.0f}s)", flush=True)
            if 9 <= cps <= 21: break   # fala natural em pt: ~12-17 car/s
        ta.save(p, w, m.sr)
print("VOZ_PRONTA", flush=True)
