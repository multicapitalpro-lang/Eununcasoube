"""Baixa os clipes do Pixabay escolhidos e recorta para 9:16.
Uso: PIXABAY_KEY=... python3 prep_clips.py <picks.json> <videos_dir> <cand.json>"""
import json, os, sys, subprocess
picks = json.load(open(sys.argv[1])); root = sys.argv[2]; cand = json.load(open(sys.argv[3]))
for p in picks:
    h = cand[p["cand"]][p["i"]]; v = p["video"]; sc = p["scene"]
    T = json.load(open(f"{root}/{v}/proj/assets/times.json"))["lines"]; N = len(T)
    S = [0.0] + [T[i][0]-0.12 for i in range(1, N)] + [json.load(open(f"{root}/{v}/proj/assets/times.json"))["total"]]
    slot = S[sc+1]-S[sc]
    q = "large" if h["wh"].get("large", (9999,))[0] <= 2200 else "medium"
    if q not in h["v"]: q = "medium" if "medium" in h["v"] else "small"
    src = f"/tmp/pxdl_{h['id']}.mp4"
    if not os.path.exists(src): subprocess.run(["curl", "-s", "-m", "180", "-o", src, h["v"][q]], check=True)
    w, hh = h["wh"][q]
    if w >= hh:  # horizontal: recorta 9:16
        z = p.get("zoom", 1.0); ch = int(hh*z)//2*2; cw = int(ch*9/16)//2*2
        vf = f"crop={cw}:{ch}:(iw-{cw})*{p.get('x',0.5)}:(ih-{ch})/2,scale=1080:1920:flags=lanczos,fps=30"
    else: vf = "scale=1080:1920:flags=lanczos,fps=30"
    out = f"{root}/{v}/proj/assets/clip-s{sc}.mp4"
    subprocess.run(["ffmpeg","-y","-v","error","-stream_loop","-1","-ss",str(p.get("ss",0)),"-t",f"{slot+0.5:.2f}","-i",src,"-an","-vf",vf,"-c:v","libx264","-crf","21","-pix_fmt","yuv420p",out], check=True)
    print(v, sc, h["id"], f"slot {slot:.1f}s", q)

# créditos (reescreve por vídeo)
cr = {}
for p in picks: cr.setdefault(p["video"], []).append(f"- clip-s{p['scene']}.mp4: {cand[p['cand']][p['i']]['page']}")
for v, ls in cr.items(): open(f"{root}/{v}/proj/assets/CREDITOS-MIDIA.md", "w").write("# Créditos de mídia (Pixabay; confira a licença atual antes de monetizar)\n" + "\n".join(ls) + "\n")
