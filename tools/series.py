#!/usr/bin/env python3
"""阿維每週市場筆記：更新「本週數字」四格走勢線（1 年／5 年）。

走勢數據放喺 index.html 入面 <script type="application/json" id="series">。
每條線 = 60 個月底收市價 + 1 個「本週」點（最後一點）。

每星期（寫完本週數字之後）喺 repo 根目錄跑：
    python3 tools/series.py week --date 2026-11-27 --spx 6950 --tnx 4.85 --brent 90.5 --hsi 22600

    - 只係換最後一點（本週收市）、標籤（例如「11月27日」）同圖下註腳嘅日期。

每個月第一期（上個月月底收市價出咗）先跑 month，再跑 week：
    python3 tools/series.py month --ym 2026-11 --spx 7000 --tnx 4.80 --brent 91.2 --hsi 22800

    - 將上個月（--ym）月底收市價加入，刪走最舊一個月，令佢永遠保持 60 個月。
    - 重複跑同一個 --ym 唔會加兩次。

數據來源（同 SOP 一致）：
    spx   標普 500 月底收市：StatMuse / 美聯社
    tnx   美國 10 年期債息月底：FRED DGS10（月度、期末）
    brent 布蘭特油價月底：FRED DCOILBRENTEU（現貨，期末）；本週點用期貨結算價
    hsi   恒指月底收市：Yahoo Finance ^HSI 月度 / 新聞收市價

檢查：python3 tools/series.py show
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
PAT = re.compile(r'(<script type="application/json" id="series">)(.*?)(</script>)', re.S)
KEYS = ["spx", "tnx", "brent", "hsi"]


def load(page):
    s = page.read_text(encoding="utf-8")
    m = PAT.search(s)
    if not m:
        sys.exit("搵唔到 <script id=\"series\">，請用最新範本。")
    return s, m, json.loads(m.group(2))


def save(page, s, m, data):
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    page.write_text(s[:m.start(2)] + body + s[m.end(2):], encoding="utf-8")


def next_ym(ym):
    y, mo = int(ym[:4]), int(ym[5:7])
    mo += 1
    if mo == 13:
        y, mo = y + 1, 1
    return f"{y}-{mo:02d}"


def last_month_in_series(d):
    # start + 59 months = latest month-end in the series
    y, mo = int(d["start"][:4]), int(d["start"][5:7]) - 1 + (len(d["v"]) - 2)
    return f"{y + mo // 12}-{mo % 12 + 1:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["week", "month", "show"])
    ap.add_argument("--page", default=str(PAGE))
    ap.add_argument("--date")
    ap.add_argument("--ym")
    for k in KEYS:
        ap.add_argument("--" + k, type=float)
    a = ap.parse_args()
    page = Path(a.page)
    s, m, data = load(page)

    if a.cmd == "show":
        for k in KEYS:
            d = data[k]
            print(f"{k}: {d['start']} 起，{len(d['v']) - 1} 個月底 + 本週（{d['end']}）= {d['v'][-1]}；最新月底 {last_month_in_series(d)} = {d['v'][-2]}")
        return

    missing = [k for k in KEYS if getattr(a, k) is None]
    if missing:
        sys.exit("缺少數字：" + ", ".join(missing))

    if a.cmd == "week":
        if not a.date or not re.match(r"\d{4}-\d{2}-\d{2}$", a.date):
            sys.exit("--date 要寫 YYYY-MM-DD（上星期五收市日）")
        label = f"{int(a.date[5:7])}月{int(a.date[8:10])}日"
        for k in KEYS:
            data[k]["v"][-1] = getattr(a, k)
            data[k]["end"] = label
        nice = f"{int(a.date[5:7])} 月 {int(a.date[8:10])} 日"
        s = re.sub(r"最後一點為 [0-9]+ 月 [0-9]+ 日收市", "最後一點為 " + nice + "收市", s)
        m = PAT.search(s)
    else:
        if not a.ym or not re.match(r"\d{4}-\d{2}$", a.ym):
            sys.exit("--ym 要寫 YYYY-MM（啱啱完咗嗰個月）")
        for k in KEYS:
            d = data[k]
            latest = last_month_in_series(d)
            if a.ym <= latest:
                print(f"{k}: {a.ym} 已經喺度，跳過")
                continue
            if a.ym != next_ym(latest):
                sys.exit(f"{k}: 最新月底係 {latest}，下一個應該係 {next_ym(latest)}，唔係 {a.ym}")
            cur = d["v"].pop()
            d["v"].append(getattr(a, k))
            d["v"].append(cur)
            d["v"].pop(0)
            d["start"] = next_ym(d["start"])
    save(page, s, m, data)
    print("已更新", page)


if __name__ == "__main__":
    main()
