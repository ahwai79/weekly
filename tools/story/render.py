"""Render HTML boards to PNG with local Chrome. Usage: python3 render.py file.html WxH out.png [...]"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

args = sys.argv[1:]
jobs = [(args[i], args[i + 1], args[i + 2]) for i in range(0, len(args), 3)]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for src, size, out in jobs:
        w, h = (int(x) for x in size.split("x"))
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg.goto(Path(src).resolve().as_uri())
        pg.wait_for_timeout(300)
        over = pg.evaluate("""() => { const b=document.querySelector('.board'); const out=[];
          b.querySelectorAll('*').forEach(e=>{ if(e.closest('.deco')) return; const r=e.getBoundingClientRect();
            if(r.width && (r.bottom>b.clientHeight+1 || r.right>b.clientWidth+1)) out.push(e.tagName+'.'+e.className+' '+Math.round(r.bottom)+'/'+Math.round(r.right)); });
          return out.slice(0,8); }""")
        if over:
            print("OVERFLOW", out, over)
        pg.screenshot(path=out, clip={"x": 0, "y": 0, "width": w, "height": h})
        print("ok", out)
    b.close()
