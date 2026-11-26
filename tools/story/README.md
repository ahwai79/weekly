# IG Story 三格（品牌版，2026-11-26 起）

每期三張 1080×1920 PNG，用 Team Servant 品牌色同字體，文字用淺白書面語。

| 檔案 | 底色 | 內容 |
|---|---|---|
| `w1.html` | 深綠 | Hook：本週一個大數字 + 一個對比數字 chip，底寫「→」 |
| `w2.html` | 沙色 | 對比／問題：兩個相關數字 + 一條問題，中間留空位貼 IG 投票貼紙 |
| `w3.html` | 深藍 | CTA：「每星期一分鐘看懂市場」+「回覆「筆記」」+ 網址 + 免責小字 |

## 每期點改

1. 打開 `w1.html`、`w2.html`、`w3.html`，只改文字同數字（同本期網頁、主圖一致）。
2. 插圖：每格 1–3 個，用 `illus.py` 入面嘅 SVG（例如 storm、line_down、bars_up、arrow_doodle、anchor、calendar、coins、sparkle、price_tag），按本週主題換；直接改 `</div></body></html>` 前面嗰幾個插圖元素。插圖唔可以蓋住字，第 2 格中間空位要留俾投票貼紙。
3. 出圖（喺呢個資料夾）：

```
python3 render.py w1.html 1080x1920 story-1.png w2.html 1080x1920 story-2.png w3.html 1080x1920 story-3.png
```

有字爆出框會印 `OVERFLOW`，要改到冇為止；出完自己睇一次先交。PNG 唔好 commit 入 repo。

字體：數字同英文用 `fonts/` 入面嘅 Fustat；中文用本機 Noto Sans CJK。
