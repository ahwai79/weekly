"""Flat brand-colour illustrations (SVG strings) for Story frames and pages.
Palette: green #05414c, sage #d4e0d9, navy #132f4c, sand #e9e0d3, white #ffffff, black #161616.
Every function returns an <svg> sized by the caller through style (left/top/width)."""

G, S, N, D, W, K = "#05414c", "#d4e0d9", "#132f4c", "#e9e0d3", "#ffffff", "#161616"
FONT = "font-family:'Noto Sans CJK HK','Noto Sans TC',sans-serif"
NUMF = "font-family:'Fustat','Noto Sans CJK HK',sans-serif"


def wrap(body, vb, style, cls="ill"):
    return f'<svg class="{cls}" viewBox="{vb}" style="{style}" aria-hidden="true">{body}</svg>'


def payslip(style, amount="+1.44%", ink=G, stamp=G):
    b = f"""
<g transform="rotate(-6 160 200)">
 <rect x="40" y="40" width="240" height="320" rx="18" fill="#0b2d34" opacity=".25" transform="translate(10 14)"/>
 <rect x="40" y="40" width="240" height="320" rx="18" fill="{W}"/>
 <rect x="40" y="40" width="240" height="64" rx="18" fill="{S}"/>
 <rect x="40" y="86" width="240" height="18" fill="{S}"/>
 <text x="66" y="84" style="{FONT};font-weight:900;font-size:30px" fill="{ink}">糧單</text>
 <rect x="66" y="132" width="150" height="12" rx="6" fill="{D}"/>
 <rect x="66" y="160" width="188" height="12" rx="6" fill="{D}"/>
 <rect x="66" y="188" width="120" height="12" rx="6" fill="{D}"/>
 <line x1="66" y1="226" x2="254" y2="226" stroke="{D}" stroke-width="3" stroke-dasharray="8 8"/>
 <text x="66" y="268" style="{FONT};font-weight:700;font-size:22px" fill="{ink}">加薪</text>
 <text x="254" y="270" text-anchor="end" style="{NUMF};font-weight:600;font-size:34px" fill="{ink}">{amount}</text>
 <rect x="66" y="296" width="80" height="12" rx="6" fill="{D}"/>
</g>
<g transform="rotate(-6 160 200)"><g transform="rotate(16 214 312)">
 <circle cx="214" cy="312" r="40" fill="none" stroke="{stamp}" stroke-width="5" opacity=".85"/>
 <circle cx="214" cy="312" r="32" fill="none" stroke="{stamp}" stroke-width="2" opacity=".85"/>
 <text x="214" y="306" text-anchor="middle" style="{FONT};font-weight:900;font-size:16px" fill="{stamp}">明年</text>
 <text x="214" y="326" text-anchor="middle" style="{FONT};font-weight:900;font-size:16px" fill="{stamp}">加幾多</text>
</g></g>"""
    return wrap(b, "0 0 380 440", style)


def price_tag(style, text="+1.9%", fill=D, ink=G):
    b = f"""
<g transform="rotate(12 140 110)">
 <path d="M60 40 H200 a14 14 0 0 1 14 14 V166 a14 14 0 0 1 -14 14 H60 L20 110 Z" fill="#0b2d34" opacity=".22" transform="translate(8 10)"/>
 <path d="M60 40 H200 a14 14 0 0 1 14 14 V166 a14 14 0 0 1 -14 14 H60 L20 110 Z" fill="{fill}"/>
 <circle cx="62" cy="110" r="11" fill="{W}"/>
 <path d="M51 110 C 20 110, 10 60, 40 30" stroke="{ink}" stroke-width="4" fill="none" stroke-linecap="round"/>
 <text x="142" y="98" text-anchor="middle" style="{FONT};font-weight:700;font-size:22px" fill="{ink}">物價</text>
 <text x="142" y="140" text-anchor="middle" style="{NUMF};font-weight:600;font-size:38px" fill="{ink}">{text}</text>
</g>"""
    return wrap(b, "0 0 240 220", style)


def sparkle(style, fill=S):
    p = "M50 0 C54 34 66 46 100 50 C66 54 54 66 50 100 C46 66 34 54 0 50 C34 46 46 34 50 0 Z"
    return wrap(f'<path d="{p}" fill="{fill}"/>', "0 0 100 100", style)


def arrow_doodle(style, color=G, flip=False):
    t = ' transform="scale(-1 1) translate(-220 0)"' if flip else ""
    b = f"""<g{t} fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
<path d="M20 30 C 90 10, 170 40, 180 130"/>
<path d="M150 112 L 181 136 L 200 100"/></g>"""
    return wrap(b, "0 0 220 160", style)


def coins(style):
    b = ""
    for i, y in enumerate([150, 126, 102, 78]):
        b += f'<ellipse cx="90" cy="{y+12}" rx="62" ry="18" fill="#0b2d34" opacity=".18"/>' if i == 0 else ""
        b += f'<rect x="28" y="{y-10}" width="124" height="22" fill="{"#c9bba6" if i%2 else D}"/>'
        b += f'<ellipse cx="90" cy="{y+12}" rx="62" ry="16" fill="#c9bba6"/>'
        b += f'<ellipse cx="90" cy="{y-10}" rx="62" ry="16" fill="{D}"/>'
    b += f'<text x="90" y="74" text-anchor="middle" style="{NUMF};font-weight:600;font-size:22px" fill="{G}">$</text>'
    return wrap(b, "0 0 180 190", style)


def chat_bubble(style, text="加薪", fill=W, ink=G):
    b = f"""
<path d="M30 20 H250 a24 24 0 0 1 24 24 V120 a24 24 0 0 1 -24 24 H110 L64 186 L72 144 H30 a24 24 0 0 1 -24 -24 V44 a24 24 0 0 1 24 -24 Z" fill="#0b2d34" opacity=".25" transform="translate(8 10)"/>
<path d="M30 20 H250 a24 24 0 0 1 24 24 V120 a24 24 0 0 1 -24 24 H110 L64 186 L72 144 H30 a24 24 0 0 1 -24 -24 V44 a24 24 0 0 1 24 -24 Z" fill="{fill}"/>
<text x="140" y="104" text-anchor="middle" style="{FONT};font-weight:900;font-size:52px" fill="{ink}">{text}</text>"""
    return wrap(b, "0 0 290 200", style)


def phone(style):
    b = f"""
<rect x="20" y="10" width="150" height="270" rx="26" fill="#0b2d34" opacity=".3" transform="translate(8 10)"/>
<rect x="20" y="10" width="150" height="270" rx="26" fill="{K}"/>
<rect x="30" y="34" width="130" height="222" rx="12" fill="{W}"/>
<rect x="72" y="18" width="46" height="8" rx="4" fill="#333"/>
<rect x="42" y="54" width="80" height="26" rx="13" fill="{S}"/>
<rect x="68" y="92" width="80" height="26" rx="13" fill="{G}"/>
<rect x="42" y="130" width="96" height="26" rx="13" fill="{S}"/>
<rect x="56" y="168" width="92" height="26" rx="13" fill="{G}"/>
<circle cx="140" cy="232" r="14" fill="{G}"/><path d="M134 232 h12 M140 226 v12" stroke="{W}" stroke-width="3" stroke-linecap="round"/>"""
    return wrap(b, "0 0 200 300", style)


def storm(style):
    b = f"""
<g fill="{S}">
 <circle cx="90" cy="90" r="46"/><circle cx="150" cy="70" r="60"/><circle cx="210" cy="96" r="42"/>
 <rect x="60" y="90" width="190" height="48" rx="24"/>
</g>
<path d="M150 140 L130 190 H156 L140 236 L188 170 H160 L176 140 Z" fill="{D}"/>
<g stroke="{S}" stroke-width="6" stroke-linecap="round" opacity=".8">
 <line x1="80" y1="160" x2="70" y2="190"/><line x1="110" y1="170" x2="100" y2="200"/>
 <line x1="210" y1="160" x2="200" y2="190"/><line x1="236" y1="150" x2="226" y2="180"/>
</g>"""
    return wrap(b, "0 0 300 250", style)


def bars_up(style, color=G):
    b = f"""
<rect x="10" y="150" width="220" height="6" rx="3" fill="{color}" opacity=".35"/>
<rect x="24" y="110" width="40" height="40" rx="6" fill="{color}" opacity=".45"/>
<rect x="80" y="84" width="40" height="66" rx="6" fill="{color}" opacity=".65"/>
<rect x="136" y="52" width="40" height="98" rx="6" fill="{color}" opacity=".85"/>
<rect x="192" y="18" width="40" height="132" rx="6" fill="{color}"/>
<path d="M30 92 L100 62 L150 40 L212 6" stroke="{color}" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M196 4 L214 4 L212 22" stroke="{color}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>"""
    return wrap(b, "0 0 240 160", style)


def line_down(style, color=S):
    b = f"""
<path d="M10 30 L70 50 L110 36 L160 90 L200 80 L250 140" stroke="{color}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M226 140 L252 142 L250 116" stroke="{color}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>"""
    return wrap(b, "0 0 270 160", style)


def calendar(style, day="星期一"):
    b = f"""
<rect x="20" y="30" width="200" height="190" rx="22" fill="#0b2d34" opacity=".3" transform="translate(8 10)"/>
<rect x="20" y="30" width="200" height="190" rx="22" fill="{W}"/>
<path d="M20 52 a22 22 0 0 1 22 -22 H198 a22 22 0 0 1 22 22 V82 H20 Z" fill="{S}"/>
<rect x="64" y="14" width="14" height="40" rx="7" fill="{N}"/><rect x="162" y="14" width="14" height="40" rx="7" fill="{N}"/>
<text x="120" y="72" text-anchor="middle" style="{FONT};font-weight:700;font-size:26px" fill="{G}">逢</text>
<text x="120" y="170" text-anchor="middle" style="{FONT};font-weight:900;font-size:58px" fill="{G}">{day}</text>"""
    return wrap(b, "0 0 240 240", style)


def underline(style, color=S):
    return wrap(f'<path d="M6 18 C 80 6, 200 4, 294 14" stroke="{color}" stroke-width="12" fill="none" stroke-linecap="round"/>', "0 0 300 28", style)


def anchor(style, color=S):
    b = f"""<g fill="none" stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
<circle cx="100" cy="34" r="18"/><line x1="100" y1="52" x2="100" y2="186"/><line x1="66" y1="84" x2="134" y2="84"/>
<path d="M30 130 C 36 172, 70 190, 100 190 C 130 190, 164 172, 170 130"/><path d="M20 140 L30 126 L44 140"/><path d="M156 140 L170 126 L180 140"/></g>"""
    return wrap(b, "0 0 200 210", style)
