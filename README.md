# Teltech Networks, S.A.: marketing site

Static HTML, CSS and vanilla JavaScript. There is no build step and there are no dependencies.

## Open it

- Double-click `index.html`. It works from `file://`.
- Or serve the folder with any static server, for example:

  ```bash
  python -m http.server 8080
  ```

  Then open http://localhost:8080. Cross-page fade transitions use native
  View Transitions over http(s) and a JS fallback on `file://`.

## Structure

```
index.html              Inicio (animated hero, verticals, 9-service grid, partners, newsletter)
telcos-isp.html         Vertical: Telcos e ISP (scroll-driven story)
empresas.html           Vertical: Empresas (scroll-driven story)
gobierno.html           Vertical: Gobierno (scroll-driven story)
soluciones.html         13 services: what it is, what it delivers, verticals, CTA
compania.html           History / team / certifications / values (pending client content)
noticias-eventos.html   News + events with empty states
reserva.html            "Agenda una reunión" request form (no calendar integration)
contacto.html           Contact details, map placeholder, quote form (#cotizacion)
css/tokens.css          ALL colors, fonts, sizes, motion values. Edit the palette here.
css/main.css            Layout and components (mobile-first)
js/main.js              Intro, nav, kinetic type, reveals, counters, horizontal track,
                        marquee, hover effects, page transitions, form validation
js/globe.js             Home hero: dot-matrix globe (Natural Earth) with arcs to the
                        five operation points + static SVG fallback logic
js/globe-data.js        Compact globe dataset (generated, ~25 KB)
js/story.js             CSS-3D isometric scroll stories on the vertical pages
fonts/                  Saira (variable wght+wdth) + IBM Plex Sans, SIL OFL 1.1, WOFF2
img/favicon.svg         Client logo on brand navy
img/partners/*.webp     Manufacturer logos, white monochrome, lazy-loaded
content/CLAIMS_TO_CONFIRM.md   Must be answered by the client before launch
```

## Editing notes

- **Palette.** Change the custom properties in `css/tokens.css`. The globe
  canvas reads `--c-accent`, `--c-neutral-400` and `--c-neutral-50` at load,
  so keep those colors opaque.
- **Globe data.** `tools/generator/build_globe.py` regenerates `js/globe-data.js`
  from a Natural Earth TopoJSON file (world-atlas `countries-50m.json`).
- **Header and footer** are repeated in every page, so the site needs no
  build step. To change navigation, footer or service copy once for all
  pages, edit `tools/generator/` (`common.py`, `services.py`, `page_*.py`)
  and run `python tools/generator/build_all.py`. It uses only the Python 3
  standard library and is optional: the site never needs it to open.
- **Forms.** Search for `TODO` in `js/main.js` and in each `<form data-endpoint>`
  to connect a backend.
- **Pending content** is marked in the HTML with `PENDING CLIENT CONTENT`
  comments and on the page with a "Pendiente: contenido del cliente" badge.

## Behaviour guarantees

- The globe falls back to a static SVG (same camera and data) when
  `prefers-reduced-motion: reduce`, `navigator.connection.saveData`, or
  `navigator.hardwareConcurrency <= 2`.
- The globe runs on requestAnimationFrame and pauses when off-screen or when
  the tab is hidden. Its network has 5 nodes (the operation points); the
  land texture is about 3,500 dots, halved on phones during the zoom-in.
- The intro plays once per browser session and never with reduced motion.
- Reduced motion turns off every non-essential animation. Stories render
  fully built and do not stick.
- Only `transform` and `opacity` are animated.
