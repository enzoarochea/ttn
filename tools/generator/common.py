# Optional maintenance tool: regenerates the static pages. Not needed to open the site.
# Usage: python tools/generator/build_all.py
"""Shared partials for the Teltech Networks static site (v2, brand identity)."""
import json
import math
import os
import random

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # project root
BRAND = "Teltech Networks, S.A."

NAV = [
    ("soluciones.html", "Soluciones"),
    ("telcos-isp.html", "Telcos e ISP"),
    ("empresas.html", "Empresas"),
    ("reserva.html", "Reserva"),
    ("contacto.html", "Contacto"),
]
CTA_HREF = "contacto.html#cotizacion"
CTA_LABEL = "Solicitar cotización"

ADDRESS_LINES = ["19 Avenida “A” 4-52, Zona 15", "Vista Hermosa I", "Ciudad de Guatemala, 01015"]
PBX_DISPLAY = "+502 2231 3400"
PBX_TEL = "+50222313400"
EMAIL = "info@grupottn.com"
HOURS = "Lunes a viernes, 8:00 a 17:00"
LOCATIONS = [("gt", "Guatemala", True), ("sv", "El Salvador", False), ("ni", "Nicaragua", False), ("cr", "Costa Rica", False), ("mia", "Miami", False)]

# Client logo (vector, from the client's current website). White via currentColor.
LOGO_PATHS = (
    '<path d="m666.958 147.212 13.51-1.99c85.053-2.071 170.908-3.836 255.949-.969 77.184 2.602 185.356 11.785 251.849 53.151 123.463 76.807-53.048 186.513-118.637 222.979C949.87 486.966 817.21 532.888 688.006 577.761l-11.044.441 74.671-31.814c68.811-30.95 136.494-64.261 202.814-100.179l-1.777-.798c-91.991 44.575-187.404 82.721-284.194 115.819-13.726 4.694-36.156 14.149-49.251 16.748-2.73.542-5.526.156-8.267.223 1.601-2.143 5.519-3.429 8.014-4.476 44.147-18.533 88.126-37.034 131.367-57.633 32.828-15.639 66.507-32.365 98.639-49.361 3.152-1.667 7.432-3.845 10.333-5.667 1.017-.639 3.082-2.064.167-1.839-70.816 33.602-144.132 62.575-218.001 89.004-23.149 8.282-47.18 17.021-70.557 24.443-7.804 2.478-15.852 6.134-23.957 5.528l71.668-30.817c112.356-52.744 228.977-106.176 329.641-179.359 29.566-21.494 64.804-49.133 86.077-78.923 79.791-111.74-127.422-131.451-193.899-136.883-9.863-.806-26.905-2.929-36.039-2.056-1.116.107-2.285-.055-3.032 1.037-.601.715.579 1.26.579 1.511v281l-1.5 1.5h-62l-121.5-194v194h-58.5l-1.5-1.5V148.712c0-.331 1.325-1.518 1-2.5h62.5l121.5 193v-192zm416.01 158.999c20.032-19.446 42.422-54.453 29.487-82.996-19.525-43.083-111.795-58.95-154.138-64.862-10.04-1.402-20.278-2.685-30.353-3.132l46.422 10.063c55.033 14.089 150.024 48.989 117.753 123.607-2.631 6.084-6.769 11.193-9.17 17.319Zm71.57-3.42c84.026-97.258-31.599-128.291-109.371-141.288-17.522-2.928-35.504-5.514-53.204-6.281l48.005 10.48c67.439 17.491 162.205 59.038 104.421 143.441l-12.421 16.068c7.861-7.13 15.648-14.408 22.57-22.42"/>'
    '<path d="M284.958 145.212v54h-86l-1 236h-62.5l-1.5-236h-86v-54z"/>'
    '<path d="M539.958 146.212v53h-86v234.5l-1.5 1.5h-61l-1.5-1.5v-234.5h-86v-53z"/>'
)
LOGO_VIEWBOX = "47.958 142.754 1183.083 435.518"


def logo_svg(cls="logo__mark"):
    return f'<svg class="{cls}" viewBox="{LOGO_VIEWBOX}" aria-hidden="true" focusable="false">{LOGO_PATHS}</svg>'


# ---------------------------------------------------------------- icons
ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "ciberseguridad": '<path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6l7-3z"/><circle cx="12" cy="10.5" r="1.8"/><path d="M12 12.3v3.4"/>',
    "audio-video": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/><path d="M10.5 7.6v4.8l4-2.4z"/>',
    "redes": '<circle cx="5" cy="6" r="2.2"/><circle cx="19" cy="6" r="2.2"/><circle cx="12" cy="18" r="2.2"/><path d="M7.2 6h9.6M6.2 7.9l4.6 8.2M17.8 7.9l-4.6 8.2"/>',
    "infraestructura-ti": '<rect x="4" y="3" width="16" height="7" rx="1.5"/><rect x="4" y="14" width="16" height="7" rx="1.5"/><path d="M8 6.5h.01M8 17.5h.01M12 6.5h4M12 17.5h4M12 10v4"/>',
    "seguridad": '<path d="M3 9.5l11-3.4 2 5.6-11 3.4z"/><path d="M16 9.4l4.5-1.6v5.6L16.9 12"/><path d="M8.3 13.9l.9 4.1H5"/>',
    "comunicaciones-unificadas": '<path d="M4 4h10a2 2 0 012 2v5a2 2 0 01-2 2H9l-4 3v-3H4a2 2 0 01-2-2V6a2 2 0 012-2z"/><path d="M19 8h1a2 2 0 012 2v5a2 2 0 01-2 2h-1v3l-3.5-3H12"/>',
    "telecomunicaciones": '<circle cx="12" cy="11" r="1.6"/><path d="M8.6 7.6a4.8 4.8 0 016.8 0M5.8 4.8a8.8 8.8 0 0112.4 0"/><path d="M12 12.6V21M8.5 21h7"/>',
    "servicios-administrados": '<circle cx="12" cy="12" r="3"/><path d="M19.5 12a7.5 7.5 0 01-13 5.1M4.5 12a7.5 7.5 0 0113-5.1"/><path d="M17.8 3.4v3.8H14M6.2 20.6v-3.8H10"/>',
    "automatizacion-procesos": '<rect x="3" y="4" width="7" height="5" rx="1.2"/><rect x="14" y="15" width="7" height="5" rx="1.2"/><path d="M10 6.5h5a2.5 2.5 0 012.5 2.5v6"/><path d="M15.3 12.8l2.2 2.2 2.2-2.2"/><path d="M6.5 9v5.5a2.5 2.5 0 002.5 2.5h2"/>',
    "asesoria-consultoria": '<circle cx="12" cy="12" r="9"/><path d="M15.6 8.4l-2.1 5.1-5.1 2.1 2.1-5.1z"/>',
    "ciberseguridad-monitoreo": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><path d="M12 12l6.4-6.4"/><circle cx="15.5" cy="9.6" r=".6"/>',
    "negocios-web": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M6.5 6.5h.01M9 6.5h.01"/><path d="M11 12.5l6 2.3-2.5 1-1 2.5z"/>',
    "agentes-ia": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/><path d="M12 9.3l.9 1.8 1.8.9-1.8.9-.9 1.8-.9-1.8-1.8-.9 1.8-.9z"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0112 2.5a7 7 0 017 7C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "phone": '<path d="M5 3.5h3.2l1.6 4.3-2 1.3a11 11 0 005.1 5.1l1.3-2 4.3 1.6V17a2 2 0 01-2.2 2A15.5 15.5 0 013 5.7a2 2 0 012-2.2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><path d="M8 12.3l2.7 2.7L16.2 9.5"/>',
}


def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'


ARROW = icon("arrow")


# ---------------------------------------------------------------- topology helpers

def edge(x1, y1, x2, y2, cls="e", d=None, pulse=False, extra="", thick=1.6):
    """Edge drawn as a rotated rect so it can 'draw itself' with transform: scaleX."""
    length = math.hypot(x2 - x1, y2 - y1)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    style = f' style="--d:{d}"' if d is not None else ""
    out = (f'<g transform="translate({x1:.1f} {y1:.1f}) rotate({ang:.2f})">'
           f'<rect class="{cls}" x="0" y="{-thick/2:.2f}" width="{length:.1f}" height="{thick}" rx="{thick/2:.2f}"{style}{extra}/>')
    if pulse:
        t = int(max(1400, length * 14))
        out += f'<circle class="p" r="3" style="--l:{length:.1f}px;--t:{t}ms;--d:{(d or 0)}"/>'
    return out + "</g>"


def node(x, y, r=4, cls="n", d=None, extra=""):
    style = f' style="--d:{d}"' if d is not None else ""
    return f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"{style}{extra}/>'


# ---------------------------------------------------------------- orbits (logo swoosh motif)

def orbits(rings):
    """rings: list of (tilt, yaw, inset%, speed s, direction, alpha)."""
    out = []
    for tilt, yaw, inset, spd, dirn, a in rings:
        out.append(f'<div class="orbit" style="--tilt:{tilt}deg;--yaw:{yaw}deg"><div class="orbit__spin" style="--spd:{spd}s;--dir:{dirn}">'
                   f'<div class="orbit__ring" style="--inset:{inset}%;--a:{a}"><span class="orbit__sat"></span></div></div></div>')
    return "".join(out)


def orbit_art(seed=0):
    rnd = random.Random(seed)
    rings = [
        (72, rnd.randint(-30, -10), 4, 16, "normal", 0.45),
        (64, rnd.randint(15, 35), 14, 11, "reverse", 0.35),
        (80, rnd.randint(-5, 5), 24, 8, "normal", 0.3),
    ]
    return (f'<div class="orbit-art" aria-hidden="true">{orbits(rings)}'
            f'<div class="orbit-art__core">{logo_svg("")}</div></div>')


# ---------------------------------------------------------------- static globe (fallback)
GEO = os.path.join(os.path.dirname(__file__), "globe-cache.json")
CITIES = [("Ciudad de Guatemala", 14.6349, -90.5069, True, -75, -95), ("El Salvador", 13.6929, -89.2182, False, 160, 160),
          ("Nicaragua", 12.1364, -86.2514, False, 15, 10), ("Costa Rica", 9.9281, -84.0907, False, 30, 60), ("Miami", 25.7617, -80.1918, False, -30, -150)]


def _vec(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def globe_static_svg(variant):
    """Same camera as js/globe.js at the end of its arrival animation."""
    geo = json.load(open(GEO))
    if variant == "d":
        W, H = 1440, 900
        cx, cy, R, lat0, par, fs, L = W * 0.72, H * 0.5, H * 2.0, 16.5, "xMidYMid slice", 13, 38
    else:
        W, H = 390, 844
        cx, cy, R, lat0, par, fs, L = W * 0.62, 240, W * 2.8, 18.0, "xMidYMin meet", 11, 22
    lon0 = -86.0
    la, lo = math.radians(lat0), math.radians(lon0)
    sl, cl, so, co = math.sin(la), math.cos(la), math.sin(lo), math.cos(lo)
    M = (-so, co, 0, -sl * co, -sl * so, cl, cl * co, cl * so, sl)

    def proj(v):
        x = M[0] * v[0] + M[1] * v[1] + M[2] * v[2]
        y = M[3] * v[0] + M[4] * v[1] + M[5] * v[2]
        z = M[6] * v[0] + M[7] * v[1] + M[8] * v[2]
        return cx + R * x, cy - R * y, z

    land, hot = [], []
    for lat, lon, f in geo["dots"]:
        x, y, z = proj(_vec(lat, lon))
        if z <= 0.02 or not (-3 < x < W + 3 and -3 < y < H + 3):
            continue
        (hot if f == 1 else land).append(f"M{x:.0f} {y:.0f}h0")
    borders = []
    for ring in geo["borders"]:
        pts = [proj(_vec(lat, lon)) for lat, lon in ring]
        borders.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y, z in pts) + "Z")
    hq = _vec(CITIES[0][1], CITIES[0][2])
    arcs, marks, labels = [], [], []
    for name, lat, lon, is_hq, ang_d, ang_m in CITIES:
        ang = ang_d if variant == "d" else ang_m
        b = _vec(lat, lon)
        x, y, _ = proj(b)
        if not is_hq:
            om = math.acos(min(1, sum(p * q for p, q in zip(hq, b))))
            lift = 0.016 + om * 0.5
            pts = []
            for s in range(0, 41):
                t = s / 40
                k1, k2 = math.sin((1 - t) * om) / math.sin(om), math.sin(t * om) / math.sin(om)
                hgt = 1 + lift * math.sin(math.pi * t)
                v = tuple((hq[i] * k1 + b[i] * k2) * hgt for i in range(3))
                px, py, _ = proj(v)
                pts.append(f"{px:.1f} {py:.1f}")
            arcs.append("M" + "L".join(pts))
        r = 4.5 if is_hq else 3.2
        marks.append(f'<circle class="city-ring" cx="{x:.1f}" cy="{y:.1f}" r="{r + 9}"/><circle class="city" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>')
        a = math.radians(ang)
        lx, ly = x + math.cos(a) * L, y + math.sin(a) * L
        anchor = "end" if math.cos(a) < -0.2 else ("start" if math.cos(a) > 0.2 else "middle")
        pad = -4 if anchor == "end" else (4 if anchor == "start" else 0)
        ty = ly + (-8 if math.sin(a) < -0.6 else (8 if math.sin(a) > 0.6 else 0))
        labels.append(f'<path class="lbl-line" d="M{x + math.cos(a) * 6:.1f} {y + math.sin(a) * 6:.1f}L{lx:.1f} {ly:.1f}"/>'
                      f'<text class="glb" x="{lx + pad:.1f}" y="{ty + 4:.1f}" text-anchor="{anchor}" style="font-size:{fs}px">{name.upper()}</text>')
        if is_hq:
            labels.append(f'<text class="glb glb--hq" x="{lx + pad:.1f}" y="{ty - fs + 2:.1f}" text-anchor="{anchor}" style="font-size:{fs - 2}px">SEDE CENTRAL</text>')
    limb = f'<circle class="limb" cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}"/>'
    return (f'<svg class="hero__static hero__static--{variant} globe-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="{par}" aria-hidden="true" focusable="false">'
            f'{limb}<path class="land" d="{"".join(land)}"/><path class="land land--hot" d="{"".join(hot)}"/>'
            f'<path class="border" d="{"".join(borders)}"/><path class="arc" d="{"".join(arcs)}"/>{"".join(marks)}{"".join(labels)}</svg>')


# ---------------------------------------------------------------- page chrome

def head(title, description, intro=False):
    full_title = f"{title} | {BRAND}" if title else f"{BRAND} | Integrador de soluciones tecnológicas"
    intro_js = ('try{if(m&&!sessionStorage.getItem("ttn-intro")){d.classList.add("intro-on");'
                'setTimeout(function(){d.classList.remove("intro-on")},5000)}}catch(e){}') if intro else ""
    return f"""<!doctype html>
<html lang="es-GT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#000818">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_GT">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/main.css">
<script>(function(d){{d.classList.add("js");var m=!window.matchMedia("(prefers-reduced-motion: reduce)").matches;if(m){{d.classList.add("motion");setTimeout(function(){{if(!d.classList.contains("ready"))d.classList.remove("motion")}},3000)}}{intro_js}}})(document.documentElement)</script>
</head>
"""


def intro_markup():
    return (f'<div class="intro" aria-hidden="true"><div class="intro__inner">'
            f'<span class="intro__ring"></span><span class="intro__ring intro__ring--2"></span>'
            f'{logo_svg("intro__logo")}<span class="intro__bar"><span></span></span></div></div>\n')


def header(active, intro=False):
    items = []
    for i, (href, label) in enumerate(NAV, 1):
        cur = ' aria-current="page"' if href == active else ""
        items.append(f'<li><a href="{href}" data-n="{i:02d}"{cur}>{label}</a></li>')
    home_cur = ' aria-current="page"' if active == "index.html" else ""
    return f"""<body>
{intro_markup() if intro else ""}<a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header">
  <div class="container site-header__bar">
    <a class="logo" href="index.html"{home_cur} aria-label="{BRAND}, inicio">
      {logo_svg()}
      <span class="logo__text" aria-hidden="true"><span class="logo__name">Teltech Networks</span><span class="logo__sub">S.A. · Desde 2013</span></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-panel" aria-label="Abrir menú">
      <span class="nav-toggle__bars" aria-hidden="true"><span></span><span></span><span></span></span>
    </button>
    <nav class="nav-panel" id="nav-panel" aria-label="Principal">
      <ul class="nav-list">
        {''.join(items)}
      </ul>
      <div class="nav-cta"><a class="btn btn--primary btn--sm magnetic" href="{CTA_HREF}">{CTA_LABEL}{ARROW}</a></div>
    </nav>
  </div>
</header>
"""


def footer(scripts=()):
    addr = "<br>".join(ADDRESS_LINES)
    js = "\n".join(f'<script src="js/{s}" defer></script>' for s in (*scripts, "main.js"))
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-big">
      <a class="logo" href="index.html" aria-label="{BRAND}, inicio">{logo_svg()}</a>
      <p>Conectamos, protegemos y automatizamos la región.</p>
    </div>
    <div class="footer-grid footer-grid--simple">
      <nav aria-labelledby="f-sitio">
        <h2 id="f-sitio">Sitio</h2>
        <ul class="footer-links">
          <li><a href="index.html">Inicio</a></li>
          <li><a href="soluciones.html">Soluciones</a></li>
          <li><a href="telcos-isp.html">Telcos e ISP</a></li>
          <li><a href="empresas.html">Empresas</a></li>
          <li><a href="reserva.html">Reserva online</a></li>
          <li><a href="contacto.html">Contacto</a></li>
        </ul>
      </nav>
      <div>
        <h2>Contacto</h2>
        <address class="footer-contact">
          <span>{addr}</span>
          <a href="tel:{PBX_TEL}">PBX {PBX_DISPLAY}</a>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <span>{HOURS}</span>
        </address>
      </div>
    </div>
    <div class="footer-legal">
      <p>© <span data-year>2026</span> {BRAND} Todos los derechos reservados.</p>
      <p>Ciudad de Guatemala, Guatemala</p>
    </div>
  </div>
</footer>
{js}
</body>
</html>
"""


def fiber():
    return '<div class="fiber" aria-hidden="true"><span class="fiber__line"></span><span class="fiber__node"></span></div>'


def kin(text, tag="h1", cls="", attrs=' data-kin-auto'):
    """Kinetic heading: '|' separates lines; '*word*' marks accent text."""
    lines = []
    for ln in text.split("|"):
        ln = ln.strip()
        if "*" in ln:
            parts = ln.split("*")
            ln = "".join(f'<span class="accent">{p}</span>' if i % 2 else p for i, p in enumerate(parts))
        lines.append(f'<span class="kin-line"><span>{ln}</span></span>')
    c = f' class="kin {cls}"' if cls else ' class="kin"'
    return f"<{tag}{c}{attrs}>{''.join(lines)}</{tag}>"


def page_hero(eyebrow, title, lead, crumb, art_seed, actions="", form=False):
    return f"""<section class="page-hero{' page-hero--form' if form else ''}">
  <div class="container page-hero__grid">
    <div>
      <nav class="breadcrumb" aria-label="Ruta de navegación"><ol><li><a href="index.html">Inicio</a></li><li aria-current="page">{crumb}</li></ol></nav>
      <p class="eyebrow">{eyebrow}</p>
      {kin(title)}
      <p class="lead" data-reveal>{lead}</p>
      {actions}
    </div>
    {orbit_art(art_seed)}
  </div>
</section>
"""


def cta_band(title="¿Tienes un proyecto en mente?",
             text="Cuéntanos qué necesitas y preparamos una propuesta a tu medida.",
             secondary=True):
    sec = '<a class="btn btn--ghost btn--xl" href="reserva.html">Agenda una reunión</a>' if secondary else ""
    rings = [(74, -20, 2, 40, "normal", 0.3), (68, 25, 12, 30, "reverse", 0.25), (80, 0, 22, 22, "normal", 0.2), (60, 10, 32, 18, "reverse", 0.18)]
    return f"""<section class="section" aria-labelledby="cta-title">
  <div class="container">
    <div class="megacta" data-reveal>
      <div class="megacta__orbits" aria-hidden="true">{orbits(rings)}</div>
      <p class="eyebrow">Hablemos</p>
      {kin(title, "h2", attrs=' id="cta-title"')}
      <p>{text}</p>
      <div class="btn-row">
        <a class="btn btn--primary btn--xl magnetic" href="{CTA_HREF}">{CTA_LABEL}{ARROW}</a>
        {sec}
      </div>
    </div>
  </div>
</section>
"""


def write(filename, html):
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename, len(html.encode()), "bytes")
