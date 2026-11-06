#!/usr/bin/env python3
"""阿維每週市場筆記：發佈後存檔。

用法（喺 repo 根目錄）：
    python3 tools/archive.py YYYY-MM-DD

YYYY-MM-DD 係本期出版日期。做以下幾樣（重複跑都安全）：
1. 確保主頁 index.html 喺聯絡區下面有「往期筆記」連結。
2. 將 index.html 另存做 issues/YYYY-MM-DD.html，og.png 另存做 issues/og/YYYY-MM-DD.png，
   並整一張細圖 issues/og/YYYY-MM-DD-s.jpg 俾目錄頁用。
3. 每個存檔頁頂部加「存檔」提示，WhatsApp 預覽改用嗰期自己嘅圖同網址。
4. 重新生成往期目錄 issues/index.html（最新一期連去主網址，舊期連去存檔頁）。

主網址 https://ahwai79.github.io/weekly/ 永遠係最新一期，唔受影響。
"""
import html
import re
import shutil
import sys
from pathlib import Path

BASE = "https://ahwai79.github.io/weekly/"
ROOT = Path(__file__).resolve().parent.parent
ISSUES = ROOT / "issues"
OGDIR = ISSUES / "og"

DISCLAIMER = ("【免責聲明】任何內容只作參考，並不構成任何投資建議。此網站只作知識及學術分享，"
              "絕對不會含應否買入或賣出某股票、何時出貨入貨、或按某些情況出貨入貨。"
              "於任何情況下，本人絕對不會提供任何投資建議或邀約或任何服務。")

PAST_CSS = (".past{display:flex;align-items:center;justify-content:space-between;gap:12px;"
            "background:var(--paper);border:1px solid var(--line);border-radius:14px;"
            "padding:14px 16px;color:var(--ink);text-decoration:none}"
            ".past strong{font-family:var(--serif);font-size:17px}"
            ".past span{color:var(--muted);font-size:14px}"
            ".past b{color:var(--accent);font-size:20px;line-height:1}"
            ".past:focus-visible{outline:3px solid var(--warn);outline-offset:2px}")
PAST_HTML = ('  <!-- past-link -->\n'
             f'  <a class="past" href="{BASE}issues/"><div><strong>往期筆記</strong><br>'
             '<span>之前每一期都可以重溫</span></div><b aria-hidden="true">→</b></a>\n\n')

BANNER_CSS = ('<style id="archive-css">.arch{background:var(--warn-soft);color:var(--ink);'
              'border:1px solid var(--line);border-radius:12px;padding:10px 14px;font-size:14px;'
              'line-height:1.6}.arch a{color:var(--accent);font-weight:700}</style>')


def parse(page: str):
    """由頁面攞期數標籤、出版日期、數據截至同標題。"""
    lines = re.findall(r'<div class="issue">([^<]*)</div>', page)
    meta = lines[-1] if lines else ""
    parts = [p.strip() for p in meta.split("·")]
    label = parts[0] if parts else ""
    pub = parts[1] if len(parts) > 1 else ""
    asof = parts[2] if len(parts) > 2 else ""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
    return label, pub, asof, title


def ensure_past_link(path: Path):
    page = path.read_text(encoding="utf-8")
    if "<!-- past-link -->" in page:
        return
    page = page.replace("</style>\n</head>", PAST_CSS + "\n</style>\n</head>", 1) \
        if "</style>\n</head>" in page else page.replace("</head>", f"<style>{PAST_CSS}</style>\n</head>", 1)
    if '  <footer class="fine">' not in page:
        sys.exit("搵唔到 <footer class=\"fine\">，未加往期連結")
    page = page.replace('  <footer class="fine">', PAST_HTML + '  <footer class="fine">', 1)
    path.write_text(page, encoding="utf-8")


def stamp_archive(path: Path):
    """存檔頁：加提示、改 OG。"""
    date = path.stem
    page = path.read_text(encoding="utf-8")
    label, pub, asof, title = parse(page)
    url = f"{BASE}issues/{date}.html"
    og = f"{BASE}issues/og/{date}.png" if (OGDIR / f"{date}.png").exists() else f"{BASE}og.png"
    page = re.sub(r'<meta property="og:url" content="[^"]*">',
                  f'<meta property="og:url" content="{url}">', page, count=1)
    page = re.sub(r'<meta property="og:image" content="[^"]*">',
                  f'<meta property="og:image" content="{og}">', page, count=1)
    page = re.sub(r'<meta property="og:title" content="[^"]*">',
                  f'<meta property="og:title" content="阿維每週市場筆記｜{html.escape(label)}（存檔）">', page, count=1)
    if 'id="archive-css"' not in page:
        page = page.replace("</head>", BANNER_CSS + "\n</head>", 1)
    if "<!-- archive-banner -->" not in page:
        asof_txt = f"，{asof}" if asof else ""
        banner = ('  <!-- archive-banner -->\n'
                  f'  <div class="arch">存檔頁｜{html.escape(label)}，{html.escape(pub)} 出版{html.escape(asof_txt)}。'
                  f'數字只反映當時情況。<a href="{BASE}">看最新一期 →</a>　<a href="{BASE}issues/">往期目錄</a></div>\n')
        page = page.replace('<div class="wrap">\n', '<div class="wrap">\n' + banner, 1)
    path.write_text(page, encoding="utf-8")


def thumb(date: str):
    src = OGDIR / f"{date}.png"
    dst = OGDIR / f"{date}-s.jpg"
    if not src.exists():
        return False
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        from PIL import Image
        im = Image.open(src).convert("RGB")
        im.thumbnail((600, 315))
        im.save(dst, "JPEG", quality=82, optimize=True)
    return True


def build_index():
    files = sorted(p for p in ISSUES.glob("????-??-??.html"))
    files.reverse()
    main = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r'<div class="avatar"><img src="(data:image/[^"]+)"', main)
    avatar = m.group(1) if m else ""
    css = re.search(r"<style>\n(/\* Layout.*?)</style>", main, re.S)
    tokens = re.search(r"(:root\{.*?\n\}.*?:root\[data-theme=\"dark\"\]\{.*?\n\})", css.group(1), re.S).group(1) if css else ""

    cards = []
    for i, f in enumerate(files):
        date = f.stem
        label, pub, asof, title = parse(f.read_text(encoding="utf-8"))
        latest = i == 0
        href = BASE if latest else f"{date}.html"
        has = thumb(date)
        img = (f'<img src="og/{date}-s.jpg" alt="" loading="lazy" width="600" height="315">'
               if has else '<div class="noimg"></div>')
        tag = '<span class="new">最新</span>' if latest else ""
        cards.append(
            f'    <a class="card" href="{href}">{img}<div class="body">'
            f'<div class="meta">{tag}{html.escape(label)} · {html.escape(pub)}'
            f'{" · " + html.escape(asof) if asof else ""}</div>'
            f'<div class="t">{html.escape(title)}</div></div></a>')

    page = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="阿維每週市場筆記往期目錄。">
<meta property="og:type" content="website">
<meta property="og:title" content="阿維每週市場筆記｜往期目錄">
<meta property="og:description" content="之前每一期市場筆記都可以喺呢度重溫。">
<meta property="og:image" content="{BASE}og.png">
<meta property="og:url" content="{BASE}issues/">
<title>往期筆記</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap">
<style>
{tokens}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:640px;margin:0 auto;padding:20px max(16px,env(safe-area-inset-right,0px)) 40px max(16px,env(safe-area-inset-left,0px));display:flex;flex-direction:column;gap:18px}}
.mast{{display:flex;align-items:center;gap:14px;padding-bottom:16px;border-bottom:1px solid var(--line)}}
.avatar{{width:44px;height:44px;border-radius:50%;background:var(--accent);flex:none;overflow:hidden}}
.avatar img{{width:100%;height:100%;object-fit:cover;display:block}}
.brand{{font-family:var(--serif);font-weight:700;font-size:19px;line-height:1.3}}
.sub{{font-size:13px;color:var(--muted);letter-spacing:.04em}}
h1{{font-family:var(--serif);font-size:clamp(24px,6.5vw,30px);line-height:1.3;margin:0}}
.lead{{margin:4px 0 0;color:var(--muted)}}
.list{{display:flex;flex-direction:column;gap:14px}}
.card{{display:flex;flex-direction:column;background:var(--paper);border:1px solid var(--line);border-radius:14px;overflow:hidden;color:var(--ink);text-decoration:none}}
.card img,.noimg{{display:block;width:100%;height:auto;aspect-ratio:1200/630;object-fit:cover;background:#10292C}}
.card .body{{padding:12px 16px 14px}}
.meta{{font-size:13px;color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:6px}}
.new{{background:var(--accent);color:var(--paper);font-weight:700;font-size:12px;border-radius:999px;padding:1px 9px}}
.t{{font-family:var(--serif);font-weight:700;font-size:19px;line-height:1.4;margin-top:4px}}
.card:focus-visible,.back:focus-visible{{outline:3px solid var(--warn);outline-offset:2px}}
.back{{align-self:flex-start;display:inline-flex;background:var(--accent);color:var(--paper);text-decoration:none;font-weight:700;border-radius:999px;padding:10px 20px}}
.fine{{font-size:12.5px;line-height:1.7;color:var(--muted);border-top:1px solid var(--line);padding-top:16px;display:flex;flex-direction:column;gap:8px}}
.fine strong{{color:var(--ink)}}
.fine a{{color:var(--muted)}}
@media (min-width:560px){{.card{{flex-direction:row}}.card img,.noimg{{width:220px;flex:none}}.card .body{{align-self:center}}}}
</style>
</head>
<body>
<div class="wrap">
  <header class="mast">
    <div class="avatar">{f'<img src="{avatar}" alt="阿維">' if avatar else ""}</div>
    <div>
      <div class="brand">阿維每週市場筆記</div>
      <div class="sub">環球視野 · 基本面為本</div>
    </div>
  </header>
  <div>
    <h1>往期筆記</h1>
    <p class="lead">每期數字只反映當時情況。想看最新市況，請看最新一期。</p>
  </div>
  <a class="back" href="{BASE}">看最新一期 →</a>
  <div class="list">
{chr(10).join(cards)}
  </div>
  <footer class="fine">
    <div><strong>阿維</strong>｜財富管理顧問　WhatsApp +852 6689 0491　IG <a href="https://www.instagram.com/ahwai.hk/" target="_blank" rel="noopener">@ahwai.hk</a></div>
    <div>{DISCLAIMER}</div>
  </footer>
</div>
</body>
</html>
"""
    (ISSUES / "index.html").write_text(page, encoding="utf-8")
    return len(files)


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sys.argv[1]):
        sys.exit("用法：python3 tools/archive.py YYYY-MM-DD")
    date = sys.argv[1]
    OGDIR.mkdir(parents=True, exist_ok=True)
    ensure_past_link(ROOT / "index.html")
    shutil.copyfile(ROOT / "index.html", ISSUES / f"{date}.html")
    if (ROOT / "og.png").exists():
        shutil.copyfile(ROOT / "og.png", OGDIR / f"{date}.png")
    for f in ISSUES.glob("????-??-??.html"):
        stamp_archive(f)
    n = build_index()
    print(f"完成：存檔 issues/{date}.html，目錄共 {n} 期")


if __name__ == "__main__":
    main()
