#!/usr/bin/env python3
"""볼트 「정기모임 체크리스트.md」 → 웹페이지(HTML) 한 파일. (사이트용: 상단 메뉴 포함)

사용: python3 build_checklist.py [md 경로] [출력 html 경로]
정본은 옵시디언 md다. 웹에서 누른 체크는 그 브라우저에만 저장되고 md로는 돌아가지 않는다.
"""
import html
import json
import pathlib
import re
import sys
from datetime import datetime

VAULT = pathlib.Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/WINNEXT 7기/회장비서"
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else VAULT / "정기모임 체크리스트.md"
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else \
    pathlib.Path(__file__).resolve().parent.parent / "checklist/index.html"


def parse(text):
    text = text.split("## 양식", 1)[0]
    meetings, m, ph, grp = [], None, None, None
    for line in text.splitlines():
        if line.startswith("## "):
            m = {"title": line[3:].strip(), "sub": "", "phases": []}
            meetings.append(m)
            ph = grp = None
        elif m is None:
            continue
        elif line.startswith("### "):
            ph = {"name": line[4:].strip(), "groups": []}
            m["phases"].append(ph)
            grp = None
        elif re.match(r"^\*\*.+\*\*\s*$", line) and ph:
            grp = {"name": line.strip("* "), "items": []}
            ph["groups"].append(grp)
        elif (mt := re.match(r"^- \[( |x|X)\] (.+)$", line)) and grp is not None:
            body = mt.group(2)
            text_, _, owner = body.rpartition(" — ") if " — " in body else (body, "", "")
            grp["items"].append({"done": mt.group(1) != " ", "text": text_.strip(), "owner": owner.strip()})
        elif line.strip() and not line.startswith(("#", ">", "-", "|")) and not m["phases"] and not m["sub"]:
            m["sub"] = line.strip()
    meetings = [x for x in meetings if any(g["items"] for p in x["phases"] for g in p["groups"])]
    if not meetings:
        sys.exit(f"체크 항목을 못 찾음: {SRC}")
    return meetings


def main():
    data = parse(SRC.read_text(encoding="utf-8"))
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    page = TEMPLATE.replace("{{DATA}}", json.dumps(data, ensure_ascii=False)) \
        .replace("{{STAMP}}", stamp).replace("{{SRC}}", html.escape(SRC.name))
    OUT.write_text(page, encoding="utf-8")
    n = sum(len(g["items"]) for x in data for p in x["phases"] for g in p["groups"])
    d = sum(i["done"] for x in data for p in x["phases"] for g in p["groups"] for i in g["items"])
    print(f"완료: {OUT}  (모임 {len(data)}건, 항목 {n}개 중 완료 {d}개)")


TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>WIN NEXT 정기모임 체크리스트</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>
  :root{--bg:#060a22;--bg2:#0d1a3d;--card:rgba(200,215,255,.06);--line:rgba(170,190,240,.16);
    --ink:#eef2fa;--muted:#a9b5cc;--dim:#6f7c98;--gold:#f0bf62;--red:#e4473b;--ok:#5fd39a}
  *{box-sizing:border-box;margin:0;padding:0}
  body{min-height:100vh;color:var(--ink);word-break:keep-all;-webkit-font-smoothing:antialiased;
    font-family:"Pretendard Variable",Pretendard,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
    background:radial-gradient(90% 40% at 50% 0%,#14244f 0%,var(--bg2) 35%,var(--bg) 75%) fixed,var(--bg)}
  main{max-width:900px;margin:0 auto;padding:36px 18px 60px}
  nav.top{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:28px}
  nav.top .brand{font-weight:800;letter-spacing:.14em;font-size:14px;color:var(--muted);margin-right:10px;text-decoration:none}
  nav.top .brand span{color:var(--red)}
  nav.top a.m{font-size:14px;font-weight:600;color:var(--muted);text-decoration:none;padding:7px 13px;border-radius:99px;border:1px solid var(--line)}
  nav.top a.m.on{background:var(--gold);color:#1a1405;border-color:var(--gold)}
  .mark{font-weight:800;letter-spacing:.14em;font-size:14px;color:var(--muted)} .mark span{color:var(--red)}
  h1{font-size:clamp(26px,5vw,38px);font-weight:800;margin-top:8px}
  .sub{color:var(--muted);margin-top:6px;font-size:15px}
  select{margin-top:18px;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:8px 12px;font:inherit}
  .sum{display:grid;grid-template-columns:auto 1fr;gap:22px;align-items:center;margin-top:20px;padding:22px;border-radius:18px;
    background:var(--card);border:1px solid var(--line)}
  .ring{--p:0;width:108px;height:108px;border-radius:50%;display:grid;place-items:center;
    background:conic-gradient(var(--gold) calc(var(--p)*1%),rgba(170,190,240,.14) 0)}
  .ring div{width:84px;height:84px;border-radius:50%;background:#0b1433;display:grid;place-items:center;text-align:center}
  .ring b{font-size:24px;font-weight:800;line-height:1} .ring small{font-size:12px;color:var(--muted)}
  .bars{display:grid;gap:12px}
  .bar .lab{display:flex;justify-content:space-between;font-size:14px;color:var(--muted);margin-bottom:6px}
  .bar .lab b{color:var(--ink)}
  .track{height:8px;border-radius:99px;background:rgba(170,190,240,.14);overflow:hidden}
  .fill{height:100%;background:var(--gold);border-radius:99px;transition:width .3s}
  .tabs{display:flex;gap:8px;margin:26px 0 6px}
  .tabs button{font:inherit;font-size:14px;font-weight:600;color:var(--muted);background:transparent;border:1px solid var(--line);
    padding:7px 14px;border-radius:99px;cursor:pointer}
  .tabs button.on{background:var(--gold);color:#1a1405;border-color:var(--gold)}
  h2{font-size:20px;margin:30px 0 4px;display:flex;align-items:baseline;gap:10px}
  h2 .cnt{font-size:14px;color:var(--gold);font-weight:700}
  h3{font-size:14px;color:var(--muted);font-weight:700;margin:18px 0 6px;letter-spacing:.02em}
  ul{list-style:none;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:var(--card)}
  li{display:flex;gap:12px;align-items:flex-start;padding:13px 14px;border-top:1px solid var(--line);cursor:pointer;user-select:none}
  li:first-child{border-top:0}
  li:hover{background:rgba(200,215,255,.04)}
  .box{flex:none;width:24px;height:24px;border-radius:7px;border:2px solid var(--dim);display:grid;place-items:center;margin-top:1px;transition:.15s}
  li.done .box{background:var(--ok);border-color:var(--ok)}
  li.done .box::after{content:"";width:6px;height:11px;border:solid #06301b;border-width:0 3px 3px 0;transform:rotate(45deg) translate(-1px,-1px)}
  .t{flex:1;font-size:15.5px;line-height:1.45}
  li.done .t{color:var(--dim);text-decoration:line-through;text-decoration-color:rgba(111,124,152,.6)}
  .st{flex:none;font-size:12px;font-weight:700;padding:3px 8px;border-radius:99px;margin-top:2px}
  li.done .st{color:var(--ok);background:rgba(95,211,154,.12)} li:not(.done) .st{color:var(--gold);background:rgba(240,191,98,.12)}
  .own{display:inline-block;font-size:12px;color:var(--muted);margin-left:6px}
  li.local .t::after{content:" · 웹에서 바꿈";font-size:11.5px;color:var(--red);text-decoration:none;display:inline-block}
  .hide-done li.done{display:none}
  footer{margin-top:34px;color:var(--dim);font-size:13px;line-height:1.7}
  footer button{font:inherit;font-size:13px;color:var(--muted);background:none;border:1px solid var(--line);border-radius:8px;padding:5px 10px;cursor:pointer;margin-top:6px}
  @media (max-width:560px){.sum{grid-template-columns:1fr;justify-items:center}.bars{width:100%}}
</style>
</head>
<body>
<main>
  <nav class="top"><a class="brand" href="../">WINNE<span>X</span>T 2026</a><a class="m" href="../">정기모임 아카이브</a><a class="m on" href="../checklist/">체크리스트</a></nav>
  <h1>정기모임 체크리스트</h1>
  <p class="sub" id="sub"></p>
  <select id="pick"></select>
  <section class="sum"><div class="ring" id="ring"><div><span><b id="pct">0%</b><br><small id="frac"></small></span></div></div><div class="bars" id="bars"></div></section>
  <div class="tabs"><button class="on" data-f="all">전체</button><button data-f="todo">미완료만</button></div>
  <div id="list"></div>
  <footer>정본은 옵시디언 「{{SRC}}」 · {{STAMP}} 기준으로 만든 화면<br>
    여기서 누른 체크는 이 브라우저에만 저장돼요. 옵시디언에도 반영하려면 비서에게 알려 주세요.<br>
    <button id="reset">옵시디언 상태로 되돌리기</button></footer>
</main>
<script>
const DATA = {{DATA}};
const KEY = "wn-checklist-" + "{{STAMP}}";
const local = JSON.parse(localStorage.getItem(KEY) || "{}");
const pick = document.getElementById("pick");
DATA.forEach((m, k) => pick.add(new Option(m.title.split("·")[0].trim(), k)));
pick.value = 0;
let filter = "all";
const esc = s => s.replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function state(id, base){ return id in local ? local[id] : base; }
function render(){
  const k = +pick.value, m = DATA[k];
  document.getElementById("sub").textContent = [m.title.split("·").slice(1).join("·").trim(), m.sub].filter(Boolean).join("  ·  ");
  let all = 0, done = 0, html = "", bars = "";
  m.phases.forEach((p, pi) => {
    let pa = 0, pd = 0, body = "";
    p.groups.forEach((g, gi) => {
      body += `<h3>${esc(g.name)}</h3><ul>`;
      g.items.forEach((it, ii) => {
        const id = `${k}-${pi}-${gi}-${ii}`, d = state(id, it.done);
        pa++; pd += d;
        body += `<li class="${d ? "done" : ""}${id in local ? " local" : ""}" data-id="${id}" data-base="${it.done ? 1 : 0}">
          <span class="box"></span><span class="t">${esc(it.text)}${it.owner ? `<span class="own">${esc(it.owner)}</span>` : ""}</span>
          <span class="st">${d ? "완료" : "미완료"}</span></li>`;
      });
      body += `</ul>`;
    });
    all += pa; done += pd;
    html += `<h2>${esc(p.name)} <span class="cnt">${pd} / ${pa}</span></h2>${body}`;
    bars += `<div class="bar"><div class="lab"><span>${esc(p.name.split("—")[0].trim())}</span><b>${pd} / ${pa}</b></div><div class="track"><div class="fill" style="width:${pa ? pd / pa * 100 : 0}%"></div></div></div>`;
  });
  const list = document.getElementById("list");
  list.innerHTML = html; list.className = filter === "todo" ? "hide-done" : "";
  document.getElementById("bars").innerHTML = bars;
  const pct = all ? Math.round(done / all * 100) : 0;
  document.getElementById("ring").style.setProperty("--p", pct);
  document.getElementById("pct").textContent = pct + "%";
  document.getElementById("frac").textContent = `${done} / ${all} 완료`;
}
document.getElementById("list").addEventListener("click", e => {
  const li = e.target.closest("li"); if (!li) return;
  const id = li.dataset.id, base = li.dataset.base === "1", now = !li.classList.contains("done");
  if (now === base) delete local[id]; else local[id] = now;
  localStorage.setItem(KEY, JSON.stringify(local)); render();
});
document.querySelectorAll(".tabs button").forEach(b => b.onclick = () => {
  document.querySelectorAll(".tabs button").forEach(x => x.classList.toggle("on", x === b)); filter = b.dataset.f; render();
});
pick.onchange = render;
document.getElementById("reset").onclick = () => { for (const k in local) delete local[k]; localStorage.removeItem(KEY); render(); };
render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
