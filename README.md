# A Cinematography Reference

A single-page reference to the visual grammar of cinema — shot sizes, camera angles,
camera movement, lighting, and composition — written for people building prompts for AI
image and video tools. Every entry pairs the idea with the words you would actually put
in a prompt.

**Six sections, 53 techniques:** Shot Sizes & Framing (10) · Camera Angles (10) ·
Camera Movement (12) · Lighting (12) · Composition & Framing Rules (9) ·
Matched Visual Examples (5).

Plain HTML, CSS and one small JavaScript file. No framework, no runtime build,
no dependencies.

## Run locally

```bash
python3 tools/serve.py 4173
```

Then open <http://localhost:4173>.

## Deploying

The site is the `site/` directory. `vercel.json` points Vercel at it via
`outputDirectory`, so importing this repository needs no further setup. If a deployment
ever serves the repository root instead, set **Root Directory** to `site` in the Vercel
project settings and remove `outputDirectory` from `vercel.json`.

## Repository layout

```
site/                the deployable site — copy it anywhere static
  index.html         generated; do not hand-edit
  styles.css
  app.js             lightbox, back-to-top, nav highlighting
  assets/
    logo/            the ALT mark, orange and white
    shots/    (10)   shot-size photographs
    angles/   (10)   camera-angle photographs
    examples/  (5)   composition examples
tools/
  build.py           regenerates site/index.html from content.json
  serve.py           the local static server
  _glyphs.json       41 inline diagram SVGs
  _logo-inline.html  the ALT mark prepared for inlining
  NOTES.md           build notes and design decisions
content.json         all site copy, in one structured file
```

## Editing content

All copy lives in `content.json`. Edit it, then regenerate:

```bash
python3 tools/build.py
```

`site/index.html` is generated output — changes made directly to it are lost on the next
build.

## Notes

- Photographs ship as WebP (~0.9 MB for all 25). The full-resolution masters are kept
  outside this repository.
- The ALT mark pairs solid shapes with outlined counter-shapes. Its strokes are authored
  in a 960-unit viewBox, so at UI sizes they scale below a pixel and disappear, leaving
  the mark looking broken. It is inlined rather than loaded as an `<img>`, and its
  strokes use `vector-effect: non-scaling-stroke`.
- Photo boxes declare `aspect-ratio`, so lazy-loaded images cause no layout shift.
- Back-to-top keys off an `IntersectionObserver` on the hero rather than a measured
  scroll threshold; nav highlighting reads `offsetTop` live on each scroll. Both earlier
  approaches — an rAF guard, and cached offsets — failed in ways that were invisible
  until tested.
- Copy is intentionally bilingual: English for headings and the movement and composition
  entries, Thai for the shot and angle entries and every Prompt Rule box.
