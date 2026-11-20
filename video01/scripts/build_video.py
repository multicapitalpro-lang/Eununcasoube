"""Motor genérico dos vídeos 02+ : lê spec.json (falas + cenas) e gera index.html (HyperFrames 1080x1920).
Uso: python3 -I build_video.py <spec.json> <pasta_proj>   (precisa de <proj>/assets/times.json de build_audio.py)"""
import json, sys, html
SPEC = json.load(open(sys.argv[1])); P = sys.argv[2]
T = json.load(open(f"{P}/assets/times.json")); L = T["lines"]; TOT = T["total"]; N = len(L)
S = [0.0] + [L[i][0]-0.12 for i in range(1, N)] + [TOT]
BGS = {"blue":("#33476f","#1a2540","#0f1628"),"purple":("#4a3a4e","#2a2236","#141324"),"warm":("#7a4326","#3b241e","#1a1216"),"night":("#27386a","#131b3a","#0a0f22"),"teal":("#2a5560","#16303a","#0c1a22")}
def ch(t, c): return "".join(f'<span class="ch {c}">{html.escape(x) if x!=" " else "&nbsp;"}</span>' for x in t)
def chunks(text, mx=30):
    out, cur = [], ""
    for w in text.split():
        if cur and len(cur)+1+len(w) > mx or (cur.endswith((",", ":", ".")) and len(cur) > 12): out.append(cur); cur = w
        else: cur = (cur+" "+w).strip()
    if cur: out.append(cur)
    return out
subs = []
for i, t in enumerate(SPEC["lines"]):
    cs = chunks(t); tot = sum(len(c) for c in cs); a, b = L[i]; acc = 0
    for j, c in enumerate(cs):
        s0 = a+(b-a)*acc/tot; acc += len(c); s1 = a+(b-a)*acc/tot
        if j == len(cs)-1: s1 = b+0.25
        subs.append((round(s0, 3), round(s1-s0, 3), c))
subhtml = "\n".join(f'<div class="clip sub" id="sub{k}" data-start="{s}" data-duration="{d}" data-track-index="9">{html.escape(c)}</div>' for k, (s, d, c) in enumerate(subs))
subjs = "\n".join(f'tl.fromTo("#sub{k}",{{scale:.92}},{{scale:1,duration:.18,ease:E}},{s});' for k, (s, d, c) in enumerate(subs))
bgdiv = "".join(f'<div id="bg{i}" class="bg" style="opacity:{1 if i==0 else 0};background:radial-gradient(ellipse 800px 900px at 540px 780px,{BGS[sc["bg"]][0]} 0%,{BGS[sc["bg"]][1]} 55%,{BGS[sc["bg"]][2]} 100%)"></div>' for i, sc in enumerate(SPEC["scenes"]))
bgjs = "".join(f'tl.to("#bg{i}",{{opacity:1,duration:.35,ease:"none"}},S[{i}]);' for i in range(1, N))
fm = lambda v: f"{int(round(v)):,}".replace(",", ".")
scn, js = [], []
for i, sc in enumerate(SPEC["scenes"]):
    first, last = i == 0, i == N-1
    k, b1, b2 = sc.get("kicker", ""), sc["big1"], sc.get("big2", "")
    import re as _re
    if i == 0 and len(_re.sub(r"[^\w ?$,.]", "", b2).strip()) > 9: b2 = _re.sub(r"\s*[^\w\s?$,.]+$", "", b2)
    dur = round(S[i+1]-S[i], 3)
    if first:
        w2 = len(_re.sub(r"[^\w ?$,.]", "", b2).strip())
        sizes = ((178, 64), (250, 132), (396, 150 if w2 <= 10 else 112))
    elif last: sizes = ((196, 54), (196, 132), (340, 120))
    else: sizes = ((200, 58), (290, 118), (410, 118))
    parts = ""
    if k: parts += f'<div class="t small" style="top:{sizes[0][0]}px;font-size:{sizes[0][1]}px">{ch(k,f"c{i}")}</div>'
    parts += f'<div class="t big" style="top:{sizes[1][0]}px;font-size:{sizes[1][1]}px">{ch(b1,f"c{i}")}</div>'
    if b2: parts += f'<div class="t big acc" style="top:{sizes[2][0]}px;font-size:{sizes[2][1]}px">{ch(b2,f"c{i}")}</div>'
    v = sc["viz"]; t = v["type"]; vh = ""; vj = ""
    if t == "emoji":
        vh = f'<div id="v{i}e" class="vem" style="top:620px">{v["emoji"]}</div>'
        vj = f'tl.fromTo("#v{i}e",{{scale:.3,opacity:0}},{{scale:1,opacity:1,duration:.6,ease:SP}},S[{i}]+.2);tl.to("#v{i}e",{{scale:1.12,duration:.5,yoyo:true,repeat:5,ease:"sine.inOut"}},S[{i}]+.9);'
    elif t == "counter":
        vh = f'<div id="v{i}e" class="vem" style="top:600px;font-size:170px">{v["emoji"]}</div><div id="v{i}n" class="vnum" style="top:790px">{fm(v["from"])}</div><div class="vlab" style="top:1030px">{html.escape(v["label"])}</div>'
        vj = (f'tl.fromTo("#v{i}e",{{scale:.3,opacity:0}},{{scale:1,opacity:1,duration:.6,ease:SP}},S[{i}]+.15);'
              f'const o{i}={{v:{v["from"]}}};tl.to(o{i},{{v:{v["to"]},duration:{v.get("d",2.4)},ease:"power2.inOut",onUpdate:()=>{{document.getElementById("v{i}n").textContent=fmt(o{i}.v)+"{v.get("suffix","")}"}}}},S[{i}]+.6);'
              + (f'tl.to("#v{i}n",{{color:"#ff7a1a",duration:.3}},S[{i}]+2.6);' if v.get("hot") else ""))
    elif t == "bars":
        its = v["items"]; mx = v["max"]; W = 330; gap = 40; x0 = (1080-(len(its)*W+(len(its)-1)*gap))/2
        for q, it in enumerate(its):
            h = max(40, 320*it["val"]/mx); x = x0+q*(W+gap); col = it.get("color", "#eaf1fb")
            vh += (f'<div id="v{i}b{q}" class="vbar" style="left:{x:.0f}px;top:{960-h:.0f}px;width:{W}px;height:{h:.0f}px;background:{col}"></div>'
                   f'<div id="v{i}t{q}" class="vval" style="left:{x:.0f}px;width:{W}px;top:972px;color:{col}">0</div>'
                   f'<div class="vlab" style="left:{x:.0f}px;width:{W}px;top:1040px;font-size:44px">{html.escape(it["name"])}</div>')
            vj += (f'tl.fromTo("#v{i}b{q}",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:1.0,ease:"power3.out"}},S[{i}]+{it.get("at",.5)});'
                   f'const ob{i}{q}={{v:0}};tl.to(ob{i}{q},{{v:{it["val"]},duration:1.2,ease:"power2.out",onUpdate:()=>{{document.getElementById("v{i}t{q}").textContent=fmt(ob{i}{q}.v)+"{it.get("suffix","")}"}}}},S[{i}]+{it.get("at",.5)});')
    elif t == "rings":
        vh = f'<div id="v{i}e" class="vem" style="top:700px;font-size:240px">{v["emoji"]}</div>' + "".join(f'<div id="v{i}r{q}" class="vring"></div>' for q in range(6))
        vj = f'tl.fromTo("#v{i}e",{{scale:.3,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:SP}},S[{i}]+.1);'
        for q in range(6): vj += f'tl.fromTo("#v{i}r{q}",{{scale:.25,opacity:.9}},{{scale:3.2,opacity:0,duration:1.2,ease:"power1.out"}},S[{i}]+.5+{q*.45});'
    elif t == "price":
        vh = (f'<div id="v{i}a" class="vprice" style="top:610px;font-size:120px;color:#aab7ca">{v["old"]}</div>'
              f'<div id="v{i}c" class="vprice" style="top:780px;font-size:230px">{v["new"]}</div>'
              f'<div id="v{i}o" class="vring2"></div>')
        vj = (f'tl.fromTo("#v{i}a",{{y:60,opacity:0}},{{y:0,opacity:1,duration:.5,ease:E}},S[{i}]+.2);'
              f'tl.fromTo("#v{i}c",{{scale:.4,opacity:0}},{{scale:1,opacity:1,duration:.55,ease:SP}},S[{i}]+1.0);'
              f'tl.fromTo("#v{i}o",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:SP}},S[{i}]+{v.get("ring",2.0)});')
    elif t == "scale":
        vh = (f'<div id="v{i}s" class="vcirc" style="left:290px;top:820px;width:90px;height:90px;background:#eaf1fb"></div>'
              f'<div id="v{i}l" class="vcirc" style="left:520px;top:640px;width:370px;height:370px;background:#ff7a1a"></div>'
              f'<div class="vlab" style="left:100px;width:480px;top:1040px;font-size:42px">{html.escape(v["a"])}</div>'
              f'<div class="vlab" style="left:500px;width:420px;top:1040px;font-size:42px">{html.escape(v["b"])}</div>')
        vj = (f'tl.fromTo("#v{i}s",{{scale:0}},{{scale:1,duration:.6,ease:SP}},S[{i}]+.3);'
              f'tl.fromTo("#v{i}l",{{scale:0}},{{scale:1,duration:1.0,ease:SP}},S[{i}]+1.6);')
    extra = '<div class="t" id="comm">👇 Responde nos comentários.</div>' if last else ""
    scn.append(f'<div class="clip scn" id="s{i}" data-start="{S[i]}" data-duration="{dur}" data-track-index="4" style="position:absolute;inset:0">{parts}{vh}{extra}</div>')
    if first: js.append(f'tl.fromTo(".c{i}",{{opacity:1,y:0,scale:1}},{{opacity:1,y:0,scale:1,duration:.01}},0);')
    else: js.append(f'chars(".c{i}",S[{i}]+.08,.03);')
    if not last: js.append(f'out(".c{i}",S[{i+1}]-.22);')
    js.append(vj)
    if last: js.append(f'tl.fromTo("#comm",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.5,ease:E}},S[{i}]+2.4);')
doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
:root{{--ice:#eaf1fb;--silver:#aab7ca;--acc:#ff7a1a;--font:"Nunito",sans-serif}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0d1220}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:var(--font);color:var(--ice)}}
.bg{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.ring{{position:absolute;border:3px solid rgba(234,241,251,.12);border-radius:50%}}
.ch{{display:inline-block}}.t{{position:absolute;left:0;width:1080px;text-align:center;line-height:1.05}}
.small{{font-weight:600;color:var(--ice)}}.big{{font-weight:900;letter-spacing:-2px;color:var(--ice)}}.acc{{color:var(--acc)}}
.sub{{position:absolute;left:60px;width:960px;top:1176px;text-align:center;font-weight:800;font-size:60px;line-height:1.1;color:#fff;
 text-shadow:3px 0 0 #0d1220,-3px 0 0 #0d1220,0 3px 0 #0d1220,0 -3px 0 #0d1220,2px 2px 0 #0d1220,-2px -2px 0 #0d1220,2px -2px 0 #0d1220,-2px 2px 0 #0d1220}}
.vem{{position:absolute;left:0;width:1080px;text-align:center;font-size:300px;line-height:1.1}}
.vnum{{position:absolute;left:0;width:1080px;text-align:center;font-weight:900;font-size:230px;line-height:1;color:var(--ice)}}
.vlab{{position:absolute;left:0;width:1080px;text-align:center;font-weight:700;font-size:50px;color:var(--silver)}}
.vbar{{position:absolute;border-radius:24px 24px 0 0}}
.vval{{position:absolute;text-align:center;font-weight:900;font-size:56px;line-height:1.1;white-space:nowrap}}
.vring{{position:absolute;left:440px;top:800px;width:200px;height:200px;border:10px solid var(--acc);border-radius:50%;opacity:0}}
.vprice{{position:absolute;left:0;width:1080px;text-align:center;font-weight:900;line-height:1;color:var(--ice)}}
.vring2{{position:absolute;left:472px;top:770px;width:150px;height:250px;border:10px solid var(--acc);border-radius:50%;opacity:0}}
.vcirc{{position:absolute;border-radius:50%}}
#comm{{top:1262px;font-weight:700;font-size:50px;color:var(--ice)}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOT}" data-width="1080" data-height="1920">
<div id="back" class="clip" data-start="0" data-duration="{TOT}" data-track-index="0" style="position:absolute;inset:0">
{bgdiv}
<div class="ring" id="r1" style="left:-120px;top:240px;width:380px;height:380px"></div><div class="ring" id="r2" style="left:820px;top:980px;width:300px;height:300px"></div>
<div class="ring" id="r3" style="left:760px;top:120px;width:200px;height:200px"></div><div class="ring" id="r4" style="left:-60px;top:1000px;width:240px;height:240px"></div>
</div>
{chr(10).join(scn)}
{subhtml}
<audio id="aud" src="assets/mix.wav" data-start="0" data-duration="{TOT}" data-track-index="10" data-volume="1"></audio>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
const S = {json.dumps(S)}, TOT = {TOT}; const E="power3.out", SP="back.out(1.8)";
const fmt = v => Math.round(v).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,".");
function chars(sel,t,st){{ tl.fromTo(sel,{{y:60,opacity:0,scale:.7}},{{y:0,opacity:1,scale:1,duration:.45,ease:SP,stagger:st}},t); }}
function out(sel,t){{ tl.to(sel,{{y:-70,opacity:0,duration:.2,ease:"power2.in"}},t); }}
tl.to("#r1",{{y:-260,rotation:90,duration:TOT,ease:"none"}},0).to("#r2",{{y:-300,duration:TOT,ease:"none"}},0).to("#r3",{{y:200,x:-80,duration:TOT,ease:"none"}},0).to("#r4",{{y:-220,x:120,duration:TOT,ease:"none"}},0);
{bgjs}
{chr(10).join(js)}
{subjs}
window.__timelines["main"] = tl;
</script></body></html>'''
open(f"{P}/index.html", "w").write(doc); print("ok", TOT)
