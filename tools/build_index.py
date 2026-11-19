#!/usr/bin/env python3
"""_data/meetings.json -> index.html (WIN NEXT 정기모임 아카이브).

사용: python3 tools/build_index.py
새 달 발표자료를 올리면 meetings.json 해당 줄에 "deck": "YYYY-MM/"를 넣고,
후기가 올라오면 "cafe"에 카페 글 번호를 넣은 뒤 다시 실행한다.
"""
import datetime as dt
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WD = "월화수목금토일"


def fmt(d):
    x = dt.date.fromisoformat(d)
    return x, f"{x.month:02d}.{x.day:02d}", WD[x.weekday()]


def main():
    data = json.loads((ROOT / "_data/meetings.json").read_text(encoding="utf-8"))
    cafe = data["cafe"]
    rows, nexts = [], []
    for m in sorted(data["meetings"], key=lambda m: m["date"], reverse=True):
        x, md, wd = fmt(m["date"])
        if m.get("deck") and not (ROOT / m["deck"] / "index.html").exists():
            sys.exit(f"발표자료 폴더 없음: {m['deck']}")
        e = html.escape
        sub = " · ".join(e(s) for s in (m.get("who", ""), m.get("place", "")) if s)
        links = []
        if m.get("deck"):
            links.append(f'<a class="btn deck" href="{e(m["deck"])}">발표자료</a>')
        for i, n in enumerate(m.get("cafe", [])):
            label = "카페 후기" if len(m["cafe"]) == 1 else f"카페 후기 {i + 1}"
            links.append(f'<a class="btn" href="{cafe}{int(n)}" target="_blank" rel="noopener">{label}</a>')
        rows.append(
            f'<li class="row" data-date="{m["date"]}">'
            f'<div class="when"><b>{md}</b><span>{wd}</span></div>'
            f'<div class="what"><span class="tag t-{e(m["type"])}">{e(m["type"])}</span>'
            f'<h3>{e(m["title"])}</h3>{f"<p>{sub}</p>" if sub else ""}</div>'
            f'<div class="links">{"".join(links) or "<span class=soon>예정</span>"}</div></li>'
        )
        nexts.append({"date": m["date"], "md": f"{x.month}월 {x.day}일 ({wd})",
                      "title": m["title"], "who": m.get("who", ""),
                      "place": m.get("place", ""), "time": m.get("time", "오전 10시"), "deck": m.get("deck", "")})
    page = TEMPLATE.replace("{{YEAR}}", str(data["year"])).replace("{{THEME}}", html.escape(data["theme"])) \
        .replace("{{ROWS}}", "\n".join(rows)).replace("{{NEXT}}", json.dumps(sorted(nexts, key=lambda n: n["date"]), ensure_ascii=False)) \
        .replace("{{COUNT}}", str(len(data["meetings"])))
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print(f"index.html: 모임 {len(rows)}건")


TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>WIN NEXT {{YEAR}} · 정기모임 아카이브</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>
  :root{--bg:#060a22;--bg2:#0d1a3d;--card:rgba(200,215,255,.06);--line:rgba(170,190,240,.16);
    --ink:#eef2fa;--muted:#a9b5cc;--dim:#6f7c98;--gold:#f0bf62;--gold2:#f6d38c;--red:#e4473b}
  *{box-sizing:border-box;margin:0;padding:0}
  body{min-height:100vh;color:var(--ink);word-break:keep-all;-webkit-font-smoothing:antialiased;
    font-family:"Pretendard Variable",Pretendard,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
    background:radial-gradient(90% 50% at 50% 0%,#14244f 0%,var(--bg2) 35%,var(--bg) 75%) fixed,var(--bg)}
  main{max-width:880px;margin:0 auto;padding:44px 20px 64px}
  nav.top{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:28px}
  nav.top .brand{font-weight:800;letter-spacing:.14em;font-size:14px;color:var(--muted);margin-right:10px;text-decoration:none}
  nav.top .brand span{color:var(--red)}
  nav.top a.m{font-size:14px;font-weight:600;color:var(--muted);text-decoration:none;padding:7px 13px;border-radius:99px;border:1px solid var(--line)}
  nav.top a.m.on{background:var(--gold);color:#1a1405;border-color:var(--gold)}
  header .mark{font-weight:800;letter-spacing:.14em;font-size:15px;color:var(--muted)}
  header .mark span{color:var(--red)}
  header h1{font-size:clamp(30px,6vw,46px);font-weight:800;margin-top:10px;line-height:1.15}
  header h1 em{font-style:normal;color:var(--gold)}
  header p{color:var(--muted);margin-top:10px;font-size:15px}
  .next{margin-top:32px;padding:26px 26px 24px;border-radius:20px;border:1px solid rgba(240,191,98,.45);
    background:linear-gradient(135deg,rgba(240,191,98,.16),rgba(240,191,98,.04) 60%),var(--card);position:relative}
  .next .k{font-size:13px;letter-spacing:.12em;color:var(--gold2);font-weight:700}
  .next h2{font-size:clamp(22px,4.4vw,30px);margin-top:8px}
  .next .meta{margin-top:10px;color:var(--ink);font-size:16px;line-height:1.6}
  .next .meta b{color:var(--gold)}
  .next .dday{position:absolute;top:22px;right:22px;font-weight:800;font-size:clamp(22px,5vw,34px);color:var(--gold)}
  h2.sec{margin:44px 0 14px;font-size:15px;letter-spacing:.12em;color:var(--muted);font-weight:700}
  ul{list-style:none}
  .row{display:grid;grid-template-columns:64px 1fr auto;gap:16px;align-items:center;
    padding:18px 4px;border-top:1px solid var(--line)}
  .row.past{opacity:.92}
  .row.upcoming .when b{color:var(--gold)}
  .when b{display:block;font-size:20px;font-weight:800;font-variant-numeric:tabular-nums}
  .when span{font-size:13px;color:var(--dim)}
  .what h3{font-size:17px;font-weight:700;margin-top:6px;line-height:1.35}
  .what p{font-size:14px;color:var(--muted);margin-top:4px}
  .tag{display:inline-block;font-size:11.5px;font-weight:700;padding:3px 8px;border-radius:99px;
    background:rgba(170,190,240,.12);color:var(--muted)}
  .t-인사이트{color:#9cc3ff}.t-네트워킹{color:#8fe0b5}.t-W-TED{color:#f6a3c8}.t-멘토링{color:#c4b2ff}
  .t-연말모임{color:var(--gold);background:rgba(240,191,98,.14)}
  .links{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}
  .btn{font-size:13.5px;font-weight:600;color:var(--ink);text-decoration:none;padding:8px 12px;border-radius:10px;
    border:1px solid var(--line);white-space:nowrap}
  .btn:hover{border-color:var(--gold)}
  .btn.deck{background:var(--gold);color:#1a1405;border-color:var(--gold)}
  .soon{font-size:13px;color:var(--dim)}
  footer{margin-top:36px;color:var(--dim);font-size:13px;line-height:1.7}
  @media (max-width:600px){
    .row{grid-template-columns:52px 1fr;gap:12px}
    .links{grid-column:2;justify-content:flex-start}
    .next .dday{position:static;display:block;margin-bottom:6px}
  }
</style>
</head>
<body>
<main>
  <nav class="top"><a class="brand" href="./">WINNE<span>X</span>T 2026</a><a class="m on" href="./">정기모임 아카이브</a><a class="m" href="./checklist/">체크리스트</a></nav>
  <header>
    <h1>{{YEAR}} 정기모임 <em>아카이브</em></h1>
    <p>{{THEME}} · 한 해 {{COUNT}}번의 모임</p>
  </header>
  <section class="next" id="next" hidden></section>
  <h2 class="sec">모임 기록</h2>
  <ul id="list">
{{ROWS}}
  </ul>
  <footer>발표자료는 이 사이트에서, 후기와 사진은 네이버 카페(회원 전용)에서 볼 수 있어요.</footer>
</main>
<script>
  const NEXT = {{NEXT}};
  const now = new Date(new Date().toLocaleString("en-US", {timeZone: "Asia/Seoul"}));
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const d = s => { const [y, m, dd] = s.split("-").map(Number); return new Date(y, m - 1, dd); };
  document.querySelectorAll(".row").forEach(r => r.classList.add(d(r.dataset.date) < today ? "past" : "upcoming"));
  const n = NEXT.find(x => d(x.date) >= today);
  if (n) {
    const left = Math.round((d(n.date) - today) / 86400000);
    const el = document.getElementById("next");
    const esc = s => s.replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
    el.innerHTML = `<div class="k">다음 모임</div><div class="dday">${left === 0 ? "D-DAY" : "D-" + left}</div>
      <h2>${esc(n.title)}</h2><div class="meta"><b>${esc(n.md)} ${esc(n.time)}</b>${n.place ? " · " + esc(n.place) : ""}${n.who ? "<br>" + esc(n.who) : ""}</div>${n.deck ? `<div class="links" style="justify-content:flex-start;margin-top:16px"><a class="btn deck" href="${esc(n.deck)}">발표자료 보기</a></div>` : ""}`;
    el.hidden = false;
  }
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
