"""Gera index.html do Vídeo 01 (HyperFrames, 1080x1920) a partir de times.json."""
import json, sys, re, html
P = sys.argv[1]
T = json.load(open(f"{P}/assets/times.json")); L = T["lines"]; TOT = T["total"]
S = [0.0, L[1][0]-0.12, L[2][0]-0.12, L[3][0]-0.12, L[4][0]-0.12, TOT]  # início de cada cena
def ch(txt, cls):  # letras individuais
    return "".join(f'<span class="ch {cls}">{html.escape(c) if c!=" " else "&nbsp;"}</span>' for c in txt)
LINES = ["Você provavelmente está usando seu celular de um jeito que pode estar acabando com a bateria mais rápido.",
 "Baterias de lítio não gostam de ficar constantemente em extremos, principalmente totalmente descarregadas, ou passando muito tempo em condições de calor.",
 "E tem um detalhe ainda mais importante: o calor acelera o desgaste da bateria.",
 "Por isso, deixar o celular carregando em um lugar muito quente, como dentro do carro no sol, pode ser uma péssima ideia.",
 "Agora me diz: você costuma deixar o celular carregando a noite inteira?"]
def chunks(text, mx=30):
    out, cur = [], ""
    for w in text.split():
        if cur and len(cur)+1+len(w) > mx or (cur.endswith((",", ":", ".")) and len(cur) > 12): out.append(cur); cur = w
        else: cur = (cur+" "+w).strip()
    if cur: out.append(cur)
    return out
subs = []
for i, t in enumerate(LINES):
    cs = chunks(t); tot = sum(len(c) for c in cs); a, b = L[i]; acc = 0
    for j, c in enumerate(cs):
        s0 = a + (b-a)*acc/tot; acc += len(c); s1 = a + (b-a)*acc/tot
        if j == len(cs)-1: s1 = b + 0.25
        subs.append((round(s0, 3), round(s1-s0, 3), c))
subhtml = "\n".join(f'<div class="clip sub" id="sub{k}" data-start="{s}" data-duration="{d}" data-track-index="9">{html.escape(c)}</div>' for k, (s, d, c) in enumerate(subs))
# estrelas determinísticas
seed = 12345
def lcg():
    global seed; seed = (seed*1103515245+12345) & 0x7fffffff; return seed/0x7fffffff
stars = "".join(f'<i class="star" style="left:{lcg()*1080:.0f}px;top:{lcg()*1330:.0f}px;width:{2+lcg()*4:.1f}px;height:{2+lcg()*4:.1f}px"></i>' for _ in range(34))
dur = lambda a, b: round(b-a, 3)
doc = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
:root{{--ice:#eaf1fb;--silver:#aab7ca;--graph:#1b2438;--ink:#0d1220;--acc:#ff7a1a;--font:"Nunito",sans-serif}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0d1220}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:var(--font);color:var(--ice)}}
.abs{{position:absolute}}
.bg{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
#bg1{{background:radial-gradient(ellipse 760px 900px at 540px 760px,#2c3f68 0%,#17213a 55%,#0f1628 100%)}}
#bg2{{background:radial-gradient(ellipse 800px 900px at 540px 780px,#33476f 0%,#1a2540 55%,#0f1628 100%)}}
#bg3{{background:radial-gradient(ellipse 800px 900px at 540px 780px,#4a3a4e 0%,#2a2236 55%,#141324 100%)}}
#bg4{{background:radial-gradient(ellipse 900px 900px at 540px 700px,#7a4326 0%,#3b241e 55%,#1a1216 100%)}}
#bg5{{background:radial-gradient(ellipse 760px 900px at 540px 640px,#27386a 0%,#131b3a 55%,#0a0f22 100%)}}
.ring{{position:absolute;border:3px solid rgba(234,241,251,.12);border-radius:50%}}
.star{{position:absolute;background:#eaf1fb;border-radius:50%;opacity:0}}
/* texto */
.ch{{display:inline-block;will-change:transform}}
.t{{position:absolute;left:0;width:1080px;text-align:center;line-height:1.05}}
.small{{font-weight:600;font-size:58px;color:var(--ice)}}
.big{{font-weight:900;font-size:128px;letter-spacing:-2px;color:var(--ice)}}
.acc{{color:var(--acc)}}
.sub{{position:absolute;left:60px;width:960px;top:1176px;text-align:center;font-weight:800;font-size:60px;line-height:1.1;color:#fff;
 text-shadow:3px 0 0 #0d1220,-3px 0 0 #0d1220,0 3px 0 #0d1220,0 -3px 0 #0d1220,2px 2px 0 #0d1220,-2px -2px 0 #0d1220,2px -2px 0 #0d1220,-2px 2px 0 #0d1220}}
/* iPhone */
#ph{{position:absolute;left:540px;top:800px;width:380px;height:780px}}
#glow{{position:absolute;left:-260px;top:-190px;width:900px;height:1160px;border-radius:50%;background:radial-gradient(ellipse at center,rgba(255,122,26,.55) 0%,rgba(255,122,26,0) 62%);opacity:0}}
#lite{{position:absolute;left:-200px;top:-120px;width:780px;height:1020px;border-radius:50%;background:radial-gradient(ellipse at center,rgba(150,190,255,.38) 0%,rgba(150,190,255,0) 62%);opacity:0}}
#body{{position:absolute;inset:0;border-radius:68px;background:linear-gradient(145deg,#dfe6f1 0%,#8d9ab0 28%,#3a4558 55%,#aeb9cb 100%)}}
#body:after{{content:"";position:absolute;inset:5px;border-radius:63px;background:#0b0f1a}}
#side1{{position:absolute;left:-5px;top:150px;width:6px;height:70px;border-radius:3px;background:#9aa6ba}}
#side2{{position:absolute;right:-5px;top:210px;width:6px;height:110px;border-radius:3px;background:#9aa6ba}}
#scr{{position:absolute;left:16px;top:16px;width:348px;height:748px;border-radius:54px;overflow:hidden;background:linear-gradient(170deg,#1c2a4a,#0c1226)}}
#isl{{position:absolute;left:50%;top:14px;margin-left:-60px;width:120px;height:34px;border-radius:17px;background:#05070d;z-index:5}}
.pane{{position:absolute;left:0;top:0;width:348px;height:748px}}
/* tela 1: ? */
#q{{position:absolute;left:0;width:348px;top:230px;text-align:center;font-weight:900;font-size:300px;color:var(--ice);line-height:1}}
/* bateria grande */
#bat{{position:absolute;left:44px;top:300px;width:230px;height:128px;border-radius:30px;border:8px solid var(--ice)}}
#nub{{position:absolute;left:278px;top:337px;width:20px;height:54px;border-radius:0 12px 12px 0;background:var(--ice)}}
#bfill{{position:absolute;left:54px;top:310px;height:108px;width:210px;border-radius:20px;background:var(--ice);transform-origin:left center}}
#pct{{position:absolute;left:0;width:348px;top:470px;text-align:center;font-weight:900;font-size:84px;color:var(--ice)}}
.mk{{position:absolute;font-weight:900;font-size:40px;color:var(--silver);opacity:.0;width:120px;text-align:center;top:250px}}
/* anel/bolt */
#ringsvg{{position:absolute;left:49px;top:250px}}
.bolt{{position:absolute;left:0;width:348px;text-align:center;top:322px;font-size:128px;line-height:1}}
#therm{{position:absolute;left:880px;top:430px;width:70px;height:420px}}
#thbar{{position:absolute;left:16px;top:0;width:38px;height:360px;border-radius:19px;background:rgba(234,241,251,.9)}}
#thfill{{position:absolute;left:23px;bottom:90px;width:24px;height:0;border-radius:12px 12px 0 0;background:var(--acc);transform-origin:bottom}}
#thbulb{{position:absolute;left:0;top:340px;width:70px;height:70px;border-radius:50%;background:var(--acc)}}
/* carro */
#car{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}}
#wind{{position:absolute;left:90px;top:520px;width:900px;height:350px;clip-path:polygon(9% 0,91% 0,100% 100%,0 100%);background:linear-gradient(180deg,#ffd9a0 0%,#ffb069 55%,#ff8a3d 100%)}}
#sun{{position:absolute;left:680px;top:560px;width:130px;height:130px;margin-left:0;border-radius:50%;background:#fff3d6}}
#rays{{position:absolute;left:575px;top:455px;width:340px;height:340px}}
#dash{{position:absolute;left:30px;top:850px;width:1020px;height:300px;border-radius:120px 120px 0 0;background:linear-gradient(180deg,#2b2f3d 0%,#161924 100%)}}
#dashhi{{position:absolute;left:150px;top:862px;width:780px;height:10px;border-radius:5px;background:rgba(234,241,251,.22)}}
.heat{{position:absolute;opacity:0}}
#warn{{position:absolute;left:640px;top:610px;width:120px;height:120px;border-radius:50%;background:var(--acc);color:#fff;font-weight:900;font-size:90px;text-align:center;line-height:120px;opacity:0}}
#moon{{position:absolute;left:70px;top:620px;opacity:0}}
#clock{{position:absolute;left:0;width:348px;top:250px;text-align:center;font-weight:300;font-size:120px;line-height:1;color:var(--ice)}}
#cdate{{position:absolute;left:0;width:348px;top:200px;text-align:center;font-weight:700;font-size:30px;color:var(--silver)}}
#full{{position:absolute;left:0;width:348px;top:520px;text-align:center;font-weight:900;font-size:72px}}
#comm{{top:1262px;font-weight:700;font-size:50px;color:var(--ice)}}
</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOT}" data-width="1080" data-height="1920">

<div class="clip" data-start="0" data-duration="{TOT}" data-track-index="0" style="position:absolute;inset:0">
  <div id="bg1" class="bg"></div><div id="bg2" class="bg" style="opacity:0"></div><div id="bg3" class="bg" style="opacity:0"></div>
  <div id="bg4" class="bg" style="opacity:0"></div><div id="bg5" class="bg" style="opacity:0"></div>
  <div class="ring" id="r1" style="left:-120px;top:240px;width:380px;height:380px"></div>
  <div class="ring" id="r2" style="left:820px;top:980px;width:300px;height:300px"></div>
  <div class="ring" id="r3" style="left:760px;top:120px;width:200px;height:200px"></div>
  <div class="ring" id="r4" style="left:-60px;top:1000px;width:240px;height:240px"></div>
  <div id="stars">{stars}</div>
  <svg id="moon" width="150" height="150" viewBox="0 0 150 150" class="abs" data-layout-allow-overflow><path d="M105 20a58 58 0 1 0 25 90A48 48 0 0 1 105 20z" fill="#eaf1fb"/></svg>
</div>

<!-- clipes reais (Pixabay) -->
<video id="vid1" class="clip" data-start="0" data-duration="{dur(0,S[1])}" data-track-index="1" muted playsinline src="assets/clip-escuro.mp4" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video>
<div id="sh1" class="clip" data-start="0" data-duration="{dur(0,S[1])}" data-track-index="2" style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,18,32,.66) 0%,rgba(13,18,32,.30) 42%,rgba(13,18,32,.72) 100%)"></div>
<video id="vid4" class="clip" data-start="{S[3]}" data-duration="{dur(S[3],S[4])}" data-track-index="1" muted playsinline src="assets/clip-carro.mp4" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video>
<div id="sh4" class="clip" data-start="{S[3]}" data-duration="{dur(S[3],S[4])}" data-track-index="2" style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(70,28,8,.72) 0%,rgba(255,122,26,.30) 55%,rgba(60,22,8,.70) 100%)"></div>
<video id="vid5" class="clip" data-start="{S[4]}" data-duration="{dur(S[4],S[5])}" data-track-index="1" muted playsinline src="assets/clip-noite.mp4" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video>
<div id="sh5" class="clip" data-start="{S[4]}" data-duration="{dur(S[4],S[5])}" data-track-index="2" style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,15,34,.70) 0%,rgba(10,15,34,.28) 45%,rgba(10,15,34,.66) 100%)"></div>

<!-- carro (cena 4) -->
<div class="clip" data-start="{S[3]}" data-duration="{dur(S[3],S[4])}" data-track-index="1" style="position:absolute;inset:0">
 <div id="car">
  <svg class="heat" id="h1" style="left:300px;top:560px" width="60" height="240" viewBox="0 0 60 240"><path d="M30 235C5 200 55 170 30 135S5 70 30 5" stroke="#fff3d6" stroke-width="9" fill="none" stroke-linecap="round"/></svg>
  <svg class="heat" id="h2" style="left:500px;top:530px" width="60" height="240" viewBox="0 0 60 240"><path d="M30 235C5 200 55 170 30 135S5 70 30 5" stroke="#fff3d6" stroke-width="9" fill="none" stroke-linecap="round"/></svg>
  <svg class="heat" id="h3" style="left:600px;top:560px" width="60" height="240" viewBox="0 0 60 240"><path d="M30 235C5 200 55 170 30 135S5 70 30 5" stroke="#fff3d6" stroke-width="9" fill="none" stroke-linecap="round"/></svg>
  <div id="warn">!</div>
 </div>
</div>

<!-- termômetro (cena 3) -->
<div class="clip" data-start="{S[2]}" data-duration="{dur(S[2],S[3])+0.1}" data-track-index="2" style="position:absolute;inset:0">
 <div id="therm"><div id="thbar"></div><div id="thfill"></div><div id="thbulb"></div></div>
</div>

<!-- iPhone -->
<div class="clip" data-start="0" data-duration="{TOT}" data-track-index="3" style="position:absolute;inset:0">
 <div id="ph">
  <div id="glow" data-layout-allow-overflow></div><div id="lite" data-layout-allow-overflow></div>
  <div id="body"></div><div id="side1"></div><div id="side2"></div>
  <div id="scr"><div id="isl"></div>
   <div class="pane" id="p1"><div id="q">?</div></div>
   <div class="pane" id="p2" style="opacity:0">
     <div class="mk" id="mk0" style="left:14px">0%</div><div class="mk" id="mk100" style="left:214px">100%</div>
     <div id="bat"></div><div id="nub"></div><div id="bfill"></div><div id="pct">40%</div></div>
   <div class="pane" id="p3" style="opacity:0">
     <svg id="ringsvg" width="250" height="250" viewBox="0 0 250 250"><circle cx="125" cy="125" r="108" stroke="rgba(234,241,251,.18)" stroke-width="16" fill="none"/>
       <circle id="ringp" cx="125" cy="125" r="108" stroke="#eaf1fb" stroke-width="16" fill="none" stroke-linecap="round" transform="rotate(-90 125 125)" stroke-dasharray="678.6" stroke-dashoffset="0"/></svg>
     <div class="bolt" id="bolt3">⚡</div></div>
   <div class="pane" id="p4" style="opacity:0;background:linear-gradient(170deg,#6a2f12,#2a1008)">
     <div class="bolt" id="bolt4" style="top:260px">🌡️</div></div>
   <div class="pane" id="p5" style="opacity:0">
     <div id="cdate">sábado, 20 de novembro</div><div id="clock">02:47</div>
     <div class="bolt" id="bolt5" style="top:430px;font-size:96px">⚡</div><div id="full5" class="abs" style="left:0;width:348px;top:560px;text-align:center;font-weight:900;font-size:64px">100%</div></div>
  </div>
 </div>
</div>

<!-- textos -->
<div class="clip" data-start="0" data-duration="{dur(0,S[1])}" data-track-index="4" id="s1" style="position:absolute;inset:0">
 <div class="t small" style="top:178px;font-size:64px">{ch("VOCÊ ESTÁ USANDO","c1")}</div>
 <div class="t big" style="top:250px;font-size:132px">{ch("O CELULAR","c1")}</div>
 <div class="t big acc" style="top:386px;font-size:150px">{ch("ERRADO? 😳","c1")}</div>
</div>
<div class="clip" data-start="{S[1]}" data-duration="{dur(S[1],S[2])}" data-track-index="4" id="s2" style="position:absolute;inset:0">
 <div class="t small" style="top:210px">{ch("🔋 A bateria não gosta de","c2")}</div>
 <div class="t big acc" style="top:300px;font-size:146px">{ch("EXTREMOS.","c2")}</div>
</div>
<div class="clip" data-start="{S[2]}" data-duration="{dur(S[2],S[3])}" data-track-index="4" id="s3" style="position:absolute;inset:0">
 <div class="t small" style="top:200px">{ch("E o calor é um dos","c3")}</div>
 <div class="t big" style="top:290px;font-size:118px">{ch("GRANDES","c3")}</div>
 <div class="t big acc" style="top:410px;font-size:118px">{ch("INIMIGOS.","c3")}</div>
</div>
<div class="clip" data-start="{S[3]}" data-duration="{dur(S[3],S[4])}" data-track-index="4" id="s4" style="position:absolute;inset:0">
 <div class="t small" style="top:190px;font-size:54px">{ch("☀️ Evite deixar","c4")}</div>
 <div class="t big" style="top:262px;font-size:100px">{ch("O CELULAR","c4")}</div>
 <div class="t big acc" style="top:368px;font-size:104px">{ch("ASSIM.","c4")}</div>
</div>
<div class="clip" data-start="{S[4]}" data-duration="{dur(S[4],S[5])}" data-track-index="4" id="s5" style="position:absolute;inset:0">
 <div class="t big" id="s5t" style="top:196px;font-size:132px">VOCÊ SABIA?</div>
 <div class="t big" id="s5e" style="top:340px;font-size:120px">👀</div>
 <div class="t" id="comm">👇 Responde nos comentários.</div>
</div>
{subhtml}
<audio id="aud" src="assets/mix.wav" data-start="0" data-duration="{TOT}" data-track-index="10" data-volume="1"></audio>
</div>

<script>
const tl = gsap.timeline({{paused:true}});
const S = {json.dumps(S)}, TOT = {TOT};
const E = "power3.out", SP = "back.out(1.8)";
gsap.set("#ph", {{xPercent:-50, yPercent:-50, y:70, scale:.78}});
tl.set("#ph",{{opacity:0}},0); tl.set("#ph",{{opacity:1}},S[1]); tl.set("#ph",{{opacity:0}},S[3]-.02);
// vida contínua no fundo (finita)
tl.to("#r1",{{y:-260,rotation:90,duration:TOT,ease:"none"}},0).to("#r2",{{y:-300,duration:TOT,ease:"none"}},0)
  .to("#r3",{{y:200,x:-80,duration:TOT,ease:"none"}},0).to("#r4",{{y:-220,x:120,duration:TOT,ease:"none"}},0);
function bgTo(id, t){{ tl.to("#bg"+id,{{opacity:1,duration:.35,ease:"none"}},t); }}
bgTo(2,S[1]); bgTo(3,S[2]); bgTo(4,S[3]); bgTo(5,S[4]);
function swap(from,to,t){{ tl.to(from,{{opacity:0,duration:.18}},t).to(to,{{opacity:1,duration:.18}},t); }}
function chars(sel,t,st=.035){{ tl.fromTo(sel,{{y:60,opacity:0,scale:.7}},{{y:0,opacity:1,scale:1,duration:.45,ease:SP,stagger:st}},t); }}
function out(sel,t){{ tl.to(sel,{{y:-70,opacity:0,duration:.2,ease:"power2.in"}},t); }}

/* CENA 1 — gancho: texto já visível no quadro 0; telefone sobe no escuro */
tl.fromTo(".c1",{{opacity:1,y:0,scale:1}},{{opacity:1,y:0,scale:1,duration:.01}},0);
tl.fromTo("#ph",{{y:210,scale:.66,rotation:-6}},{{y:70,scale:.78,rotation:0,duration:.9,ease:"power3.out"}},0);
tl.fromTo("#lite",{{opacity:0}},{{opacity:1,duration:1.1,ease:"power2.out"}},0.1);
tl.fromTo("#q",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:SP}},0.3);
tl.to("#q",{{scale:1.12,duration:.7,yoyo:true,repeat:3,ease:"sine.inOut"}},1.0);
tl.fromTo("#ph",{{rotation:0}},{{rotation:2.2,immediateRender:false,duration:2.4,ease:"sine.inOut",yoyo:true,repeat:1}},0.9);
out(".c1",S[1]-.22);

/* CENA 2 — extremos */
swap("#p1","#p2",S[1]);
tl.to("#ph",{{scale:.81,duration:.4,ease:SP}},S[1]);
chars(".c2",S[1]+.08,.028);
const pc={{v:40}}, setp=()=>{{const v=Math.round(pc.v);document.getElementById("pct").textContent=v+"%";gsap.set("#bfill",{{scaleX:Math.max(.02,pc.v/100)}});}};
tl.fromTo(pc,{{v:40}},{{v:100,duration:1.1,ease:"power2.inOut",onUpdate:setp}},S[1]+1.2);
tl.fromTo("#mk100",{{opacity:0,scale:.6,color:"#aab7ca"}},{{opacity:1,scale:1.15,color:"#ff7a1a",duration:.35,ease:SP}},S[1]+2.3);
tl.to("#mk100",{{opacity:.35,scale:1,duration:.3}},S[1]+3.0);
tl.fromTo(pc,{{v:100}},{{v:2,duration:1.3,ease:"power2.inOut",onUpdate:setp,immediateRender:false}},S[1]+3.3);
tl.to("#bfill",{{backgroundColor:"#ff7a1a",duration:.3}},S[1]+4.3);
tl.to("#pct",{{color:"#ff7a1a",duration:.3}},S[1]+4.3);
tl.fromTo("#mk0",{{opacity:0,scale:.6,color:"#aab7ca"}},{{opacity:1,scale:1.15,color:"#ff7a1a",duration:.35,ease:SP}},S[1]+4.6);
tl.fromTo("#bat",{{x:0}},{{x:6,duration:.07,yoyo:true,repeat:5,ease:"none"}},S[1]+4.7);
tl.to("#glow",{{opacity:1,duration:1.0,ease:"power2.out"}},S[1]+6.6);
tl.to("#ph",{{rotation:-2,duration:.6,ease:"sine.inOut",yoyo:true,repeat:1}},S[1]+6.6);
out(".c2",S[2]-.22);

/* CENA 3 — calor acelera o desgaste */
swap("#p2","#p3",S[2]);
tl.fromTo("#ph",{{x:0}},{{x:-120,scale:.76,duration:.5,ease:SP}},S[2]);
tl.fromTo("#glow",{{opacity:1}},{{opacity:.35,duration:.5}},S[2]);
chars(".c3",S[2]+.08,.03);
tl.fromTo("#therm",{{x:80,opacity:0}},{{x:0,opacity:1,duration:.5,ease:SP}},S[2]+.2);
tl.fromTo("#thfill",{{height:0}},{{height:290,duration:3.0,ease:"power1.in"}},S[2]+.7);
tl.fromTo("#ringp",{{attr:{{"stroke-dashoffset":0}},stroke:"#eaf1fb"}},{{attr:{{"stroke-dashoffset":300}},stroke:"#ff7a1a",duration:2.6,ease:"power1.inOut"}},S[2]+1.0);
tl.fromTo("#bolt3",{{scale:1}},{{scale:1.15,duration:.4,yoyo:true,repeat:5,ease:"sine.inOut"}},S[2]+.3);
out(".c3",S[3]-.22);
tl.to("#therm",{{opacity:0,x:80,duration:.25}},S[3]-.1);

/* CENA 4 — carro no sol */
swap("#p3","#p4",S[3]);
tl.fromTo("#car",{{opacity:0}},{{opacity:1,duration:.4}},S[3]);
tl.to("#ph",{{x:0,y:160,scale:.46,rotation:-7,duration:.7,ease:"power3.inOut"}},S[3]);
tl.to("#glow",{{opacity:1,duration:.6}},S[3]+.4);
chars(".c4",S[3]+.12,.03);
["#h1","#h2","#h3"].forEach((h,i)=>{{
  tl.fromTo(h,{{opacity:0,y:30}},{{opacity:.7,y:-60,duration:.9,ease:"sine.out"}},S[3]+1.4+i*.35);
  tl.to(h,{{opacity:0,y:-130,duration:.9,ease:"sine.in"}},S[3]+2.3+i*.35);
  tl.fromTo(h,{{opacity:0,y:30}},{{opacity:.7,y:-60,duration:.9,ease:"sine.out",immediateRender:false}},S[3]+3.3+i*.3);
  tl.to(h,{{opacity:0,y:-130,duration:.9,ease:"sine.in"}},S[3]+4.2+i*.3);
}});
tl.fromTo("#bolt4",{{rotation:-8}},{{rotation:8,duration:.12,yoyo:true,repeat:9,ease:"none"}},S[3]+1.5);
tl.fromTo("#warn",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.4,ease:SP}},S[3]+4.8);
out(".c4",S[4]-.22);
tl.to("#car",{{opacity:0,duration:.3}},S[4]-.05);

/* CENA 5 — noite, pergunta */
swap("#p4","#p5",S[4]);
tl.to("#ph",{{x:0,y:20,scale:.72,rotation:0,duration:.6,ease:"power3.inOut"}},S[4]);
tl.to("#glow",{{opacity:0,duration:.4}},S[4]);
tl.fromTo("#s5t",{{scale:.5,opacity:0,y:40}},{{scale:1,opacity:1,y:0,duration:.55,ease:SP}},S[4]+.15);
tl.fromTo("#s5e",{{scale:.2,opacity:0,rotation:-20}},{{scale:1,opacity:1,rotation:0,duration:.6,ease:SP}},S[4]+.55);
tl.fromTo("#bolt5",{{scale:1}},{{scale:1.2,duration:.5,yoyo:true,repeat:5,ease:"sine.inOut"}},S[4]+.6);
tl.fromTo("#comm",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.5,ease:E}},S[4]+2.7);
tl.to("#comm",{{y:-8,duration:.4,yoyo:true,repeat:1,ease:"sine.inOut"}},S[4]+3.3);

/* legendas */
document.querySelectorAll(".sub").forEach(el=>{{
  const s=parseFloat(el.dataset.start);
  tl.fromTo("#"+el.id,{{scale:.92}},{{scale:1,duration:.18,ease:E}},s);
}});
window.__timelines["main"] = tl;
</script>
</body></html>'''
open(f"{P}/index.html", "w").write(doc)
print("ok", S)
