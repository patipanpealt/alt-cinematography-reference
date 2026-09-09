# -*- coding: utf-8 -*-
"""Builds site/index.html from content.json + the diagram SVGs lifted from the source page."""
import json, io, os, re, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
content = json.load(io.open(f"{BASE}/content.json", encoding="utf-8"))
glyphs  = json.load(io.open(f"{BASE}/tools/_glyphs.json", encoding="utf-8"))
LOGO    = io.open(f"{BASE}/tools/_logo-inline.html", encoding="utf-8").read().strip()

# diagram SVGs come out of the source in document order
G = {"shots": glyphs[0:10], "angles": glyphs[10:20],
     "movement": glyphs[20:32], "composition": glyphs[32:41]}

PHOTOS = {
 "shots": ["extreme-wide","wide-long","full","medium-long-cowboy","medium",
           "medium-close-up","close-up","extreme-close-up","insert-cutaway","two-shot"],
 "angles":["eye-level","high-angle","low-angle","dutch-canted","overhead-top",
           "birds-eye","worms-eye","over-the-shoulder","pov","reverse-angle"],
}
EXAMPLE_FILES = ["rule-of-thirds","leading-lines","frame-within-a-frame",
                 "symmetry-centered","depth-layering"]

e = html.escape
def code(s):
    """`x` -> <code>x</code>, everything else escaped."""
    parts = re.split(r'`([^`]*)`', s)
    return "".join(e(p) if i % 2 == 0 else f"<code>{e(p)}</code>" for i, p in enumerate(parts))

sec = {s["id"]: s for s in content["sections"]}
out = []
w = out.append

# ---------------------------------------------------------------- head
w('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>A Cinematography Reference</title>
<meta name="description" content="A cinematography reference for AI image and video prompts: shot sizes, camera angles, movement, lighting, and composition.">
<link rel="icon" href="assets/logo/ALT-Logo-Orange.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anuphan:wght@300;400;500;600;700&family=Inter:wght@400;500;600&family=Inter+Tight:wght@600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>''')

# ---------------------------------------------------------------- nav
NAV = [("#shots","Shot Sizes &amp; Framing"), ("#angles","Camera Angles"),
       ("#movement","Camera Movement"), ("#lighting","Lighting"),
       ("#composition","Composition &amp; Framing Rules"), ("#examples","Matched Visual Examples")]
w('\n<div class="shell">')
w('\n<nav class="nav">')
w(f'  <a class="nav-logo" href="#hero" aria-label="Back to top">{LOGO}</a>')
w('  <div class="nav-links">')
for href, label in NAV:
    w(f'    <a href="{href}">{label}</a>')
w('  </div>\n</nav>')

# ---------------------------------------------------------------- hero
h = content["hero"]
w(f'''
<header class="hero" id="hero">
  <div class="hero-copy">
    <h1>A <em>Cinematography</em><br>Reference</h1>
    <p class="sub">{e(h["sub"])}</p>
  </div>
</header>''')

# ---------------------------------------------------------------- helpers
# each heading is split so the tail runs in orange, the way Color-04 two-tones its titles
TITLE_SPLIT = {
 "01": ("Shot Sizes", "&amp; Framing"),
 "02": ("Camera", "Angles"),
 "03": ("Camera", "Movement"),
 "04": ("", "Lighting"),
 "05": ("Composition", "&amp; Framing Rules"),
 "06": ("Matched Visual", "Examples"),
}
CHIP = {"01":"Shot Sizes","02":"Camera Angles","03":"Camera Movement",
        "04":"Lighting","05":"Composition","06":"Examples"}

def sec_header(num, intro, rule=None, raw_intro=False):
    lead, tail = TITLE_SPLIT[num]
    title = (f'{lead} ' if lead else '') + f'<em>{tail}</em>'
    w(f'''  <div class="sec-head">
    <span class="chip"><i></i>{num} &mdash; {CHIP[num]}</span>
    <h2>{title}</h2>
    <p class="sec-intro">{intro if raw_intro else e(intro)}</p>
  </div>''')
    if rule:
        w(f'  <div class="prompt-rule"><b>Prompt Rule</b>{code(rule)}</div>')

def head(num, title, intro, rule):
    sec_header(num, intro, rule)

def card(glyph, photo, alt, abbr, tag, name, desc, use_label, use, prompt):
    w('    <article class="card">')
    w(f'      <div class="glyph">{glyph}</div>')
    if photo:
        w(f'''      <figure class="card-photo">
        <button type="button" data-zoom aria-label="View {e(alt)} full size"><img src="{photo}" alt="{e(alt)}" loading="lazy"><span class="corner" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M7 17 17 7M9 7h8v8"/></svg></span></button>
        <figcaption>Generated matched example</figcaption>
      </figure>''')
    w(f'      <div class="card-top"><span class="tag">{e(tag)}</span>'
      + (f'<span class="abbr">{e(abbr)}</span>' if abbr else '') + '</div>')
    w(f'      <h3>{e(name)}</h3>')
    w(f'      <p>{e(desc)}</p>')
    w(f'      <div class="use"><b>{e(use_label)}</b>{e(use)}</div>')
    w(f'      <div class="prompt"><b>Prompt words</b>{e(prompt)}</div>')
    w('    </article>')

# ---------------------------------------------------------------- 01 shots
s = sec["shots"]
w('\n<section class="band" id="shots">')
head("01", s["title"], s["intro"], s["promptRule"])
w('  <div class="grid">')
for i, c in enumerate(s["cards"]):
    card(G["shots"][i], f'assets/shots/{PHOTOS["shots"][i]}.webp', f'{c["name"]} example',
         c.get("abbr"), "Shot Size", c["name"], c["desc"], "Use it for", c["use"], c["prompt"])
w('  </div>\n</section>')

# ---------------------------------------------------------------- 02 angles
s = sec["angles"]
w('\n<section class="band" id="angles">')
head("02", s["title"], s["intro"], s["promptRule"])
w('  <div class="grid">')
for i, c in enumerate(s["cards"]):
    card(G["angles"][i], f'assets/angles/{PHOTOS["angles"][i]}.webp', f'{c["name"]} camera angle example',
         None, "Angle", c["name"], c["desc"], "Feels like", c["use"], c["prompt"])
w('  </div>\n</section>')

# ---------------------------------------------------------------- 03 movement
s = sec["movement"]
w('\n<section class="band" id="movement">')
head("03", s["title"], s["intro"], s["promptRule"])
w('  <div class="grid">')
for i, c in enumerate(s["cards"]):
    card(G["movement"][i], None, None, None, "Movement",
         c["name"], c["desc"], "Use it for", c["use"], c["prompt"])
w('  </div>\n</section>')

# ---------------------------------------------------------------- 04 lighting
s = sec["lighting"]
w('\n<section class="band" id="lighting">')
head("04", s["title"], s["intro"], s["promptRule"])
w(f'''  <div class="callout">
    <h4>{e(s["callout"]["title"])}</h4>
    <p>{code(s["callout"]["body"])}</p>
  </div>
  <div class="light-grid">''')
TONES = ["cream","orange","dark"]
for i, r in enumerate(s["rows"]):
    prompt = r["prompt"].replace("ZenityX red", "deep orange")   # brand name stripped
    tone = TONES[i % 3]
    w(f'''    <article class="lcard {tone}">
      <div class="lcard-top">
        <h3>{e(r["name"])}</h3>
        <span class="lsub">{e(r["sub"])}</span>
      </div>
      <p>{e(r["desc"])}</p>
      <div class="lprompt"><b>Prompt words</b>{e(prompt)}</div>
    </article>''')
w('  </div>\n</section>')

# ---------------------------------------------------------------- 05 composition
s = sec["composition"]
w('\n<section class="band" id="composition">')
head("05", s["title"], s["intro"], s["promptRule"])
w('  <div class="grid">')
for i, c in enumerate(s["cards"]):
    card(G["composition"][i], None, None, None, c["tag"],
         c["name"], c["desc"], "Effect", c["use"], c["prompt"])
w('  </div>\n</section>')

# ---------------------------------------------------------------- 06 matched visual examples
gal = s["exampleGallery"]
OVERLAY = {
 "rule-of-thirds": '<span class="thirds-overlay" aria-hidden="true"></span>',
 "leading-lines": '''<span class="svg-overlay" aria-hidden="true"><svg viewBox="0 0 1600 1000" preserveAspectRatio="none">
        <path d="M120 1000 L760 420" stroke="#E85002" stroke-width="7" fill="none"/>
        <path d="M1480 1000 L840 420" stroke="#E85002" stroke-width="7" fill="none"/>
        <circle cx="800" cy="420" r="18" fill="#F9F9F9"/></svg></span>''',
 "frame-within-a-frame": '',
 "symmetry-centered": '<span class="center-axis" aria-hidden="true"></span>',
 "depth-layering": '''<span class="svg-overlay" aria-hidden="true"><svg viewBox="0 0 1600 1000" preserveAspectRatio="none">
        <rect x="0" y="0" width="1600" height="330" fill="rgba(232,80,2,.13)"/>
        <rect x="0" y="330" width="1600" height="330" fill="rgba(241,96,1,.13)"/>
        <rect x="0" y="660" width="1600" height="340" fill="rgba(217,195,171,.13)"/>
        <text x="52" y="120" fill="#fff" font-size="46" font-family="monospace">BACKGROUND</text>
        <text x="52" y="495" fill="#fff" font-size="46" font-family="monospace">MIDGROUND</text>
        <text x="52" y="835" fill="#fff" font-size="46" font-family="monospace">FOREGROUND</text></svg></span>''',
}
w('\n<section class="band" id="examples">')
sec_header("06", "Examples of image composition arranged according to the Composition &amp; Framing Rules above.", raw_intro=True)
w('  <div class="examples">')
for i, it in enumerate(gal["items"]):
    f = EXAMPLE_FILES[i]
    w(f'''    <article class="example-card">
      <button type="button" class="example-visual" data-zoom aria-label="View {e(it["title"])} example full size">
        <img src="assets/examples/{f}.webp" alt="{e(it["alt"])}" loading="lazy">
        {OVERLAY[f]}
      </button>
      <div class="example-copy">
        <span class="label">{e(it["label"])}</span>
        <h4>{e(it["title"])}</h4>
        <p>{e(it["copy"])}</p>
        <span class="source">Generated example</span>
      </div>
    </article>''')
w('  </div>\n</section>')

# ---------------------------------------------------------------- footer
w(f'''
<footer>
  <div class="presented">
    <span>Presented by</span>
    {LOGO}
  </div>
</footer>''')

# ---------------------------------------------------------------- overlays + scripts
w('</div>')  # /shell
w('''
<button class="to-top" id="to-top" type="button" aria-label="Back to top">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>

<div class="lightbox" id="lightbox" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Image viewer">
  <div class="lightbox-inner">
    <button class="lightbox-close" type="button" aria-label="Close">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>
    </button>
    <img id="lightbox-img" src="" alt="">
  </div>
</div>

<script src="app.js"></script>
</body>
</html>''')

doc = "\n".join(out)
io.open(f"{BASE}/site/index.html", "w", encoding="utf-8").write(doc)
print("index.html written:", len(doc), "bytes")
assert "ZenityX" not in doc, "ZenityX still present!"
print("ZenityX check: clean")
