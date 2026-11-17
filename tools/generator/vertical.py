"""Shared builder for the vertical pages (v2): CSS-3D isometric scroll stories."""
import math
from common import *
from services import ALL

SVC = {s["slug"]: s for s in ALL}
SPAN = 0.12


# ---------------------------------------------------------------- scene primitives (340 x 340 ground)

def ground(edges, nodes):
    """edges: [(x1,y1,x2,y2,t,hot)], nodes: [(x,y,r,t)] drawn flat on the ground plane."""
    parts = [edge(x1, y1, x2, y2, cls="e st-e e--hot" if hot else "e st-e", thick=3 if hot else 2, extra=f' data-t="{t}"')
             for x1, y1, x2, y2, t, hot in edges]
    parts += [node(x, y, r, cls="n st-n", extra=f' data-t="{t}"') for x, y, r, t in nodes]
    return f'<svg class="topo" viewBox="0 0 340 340">{"".join(parts)}</svg>'


def pillar(x, y, h, t, base=True):
    b = '<span class="pillar__base"></span>' if base else ""
    return (f'<div class="pillar__wrap st-p" data-t="{t}" style="left:{x}px;top:{y}px;--h:{h}px">'
            f'{b}<span class="pillar"></span><span class="pillar__cap"></span></div>')


def tag(x, y, z, t, text):
    return f'<span class="iso-tag st-tag" data-t="{t}" style="left:{x}px;top:{y}px;--tz:{z}px">{text}</span>'


def wave(x1, y1, h1, x2, y2, h2, t):
    """Wireless link drawn on an upright plane from tower 1 top to tower 2 top."""
    L = math.hypot(x2 - x1, y2 - y1)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    H = 140
    y_a, y_b = H - h1, H - h2
    peak = min(y_a, y_b) - 34
    return (f'<div class="iso-wave" style="left:{x1}px;top:{y1 - H}px;width:{L:.1f}px;transform:rotateZ({ang:.2f}deg) rotateX(-90deg)">'
            f'<svg class="st-w" data-t="{t}" viewBox="0 0 {L:.1f} {H}" preserveAspectRatio="none">'
            f'<path d="M0 {y_a} Q{L / 2:.1f} {peak} {L:.1f} {y_b}"/><circle cx="0" cy="{y_a}" r="3"/><circle cx="{L:.1f}" cy="{y_b}" r="3"/></svg></div>')


def box(x, y, w, d, h, t):
    return (f'<div class="box st-b" data-t="{t}" style="left:{x}px;top:{y}px;width:{w}px;height:{d}px;--bw:{w}px;--bd:{d}px;--bh:{h}px">'
            f'<div class="box__s"><span class="box__win"></span></div><div class="box__e"><span class="box__win"></span></div><div class="box__top"></div></div>')


def scene(inner, mod=""):
    cls = f"iso-stage {mod}".strip()
    return f'<div class="{cls}" aria-hidden="true"><div class="iso-world">{inner}</div></div>'


# ---------------------------------------------------------------- the three scenes

def scene_telcos():
    C, T1, T2 = (50, 170), (130, 115), (130, 235)
    S = [(205, 70), (215, 150), (205, 230)]
    homes = [[(275, 40), (292, 92)], [(285, 132), (296, 178)], [(278, 214), (294, 258)]]
    R = (250, 312)
    edges = [(*C, *T1, 0.02, True), (*C, *T2, 0.06, True),
             (*T1, *S[0], 0.16, False), (*T1, *S[1], 0.19, False), (*T2, *S[2], 0.22, False)]
    nodes = []
    t = 0.32
    for s, hs in zip(S, homes):
        for hpt in hs:
            edges.append((*s, *hpt, round(t, 3), False)); nodes.append((*hpt, 4, round(t + SPAN, 3))); t += 0.03
    edges += [(*R, 306, 292, 0.74, False), (*R, 296, 334, 0.77, False)]
    nodes += [(306, 292, 4, 0.86), (296, 334, 4, 0.89)]
    plane = f'<div class="iso-plane">{ground(edges, nodes)}</div>'
    towers = (pillar(*C, 96, 0.0) + pillar(*T1, 58, 0.12) + pillar(*T2, 58, 0.16)
              + "".join(pillar(*s, 40, 0.26 + i * 0.03) for i, s in enumerate(S))
              + pillar(*R, 86, 0.58))
    tags = (tag(C[0], C[1], 104, 0.02, "Central") + tag(S[1][0], S[1][1], 54, 0.3, "Red GPON")
            + tag(294, 258, 22, 0.5, "Última milla") + tag(R[0], R[1], 98, 0.7, "Zona rural"))
    return scene(plane + towers + wave(*T2, 58, *R, 86, 0.62) + tags)


def scene_empresas():
    names = [("Infraestructura TI", "infraestructura-ti"), ("Redes", "redes"), ("Ciberseguridad", "ciberseguridad"),
             ("Comunicaciones", "comunicaciones-unificadas"), ("Automatización e IA", "automatizacion-procesos")]
    layers = "".join(
        f'<div class="layer st-l" data-i="{i}" data-t="{round(i * 0.07, 2)}"><span class="layer__icon">{icon(slug)}</span>'
        f'<span class="layer__label">{n}</span></div>' for i, (n, slug) in enumerate(names))
    beams = "".join(f'<span class="beam st-beam" style="left:{x}px;top:{y - 232}px;height:232px"></span>' for x, y in [(34, 34), (306, 34), (34, 306), (306, 306), (170, 170)])
    base = '<div class="iso-plane iso-plane--faint"></div>'
    return scene(base + beams + layers + tag(170, 34, 262, 0.8, "Servicios administrados"), "iso-stage--stack")


def scene_gobierno():
    dc = (140, 140, 60, 60, 112)
    blds = [(36, 36, 56, 44, 62), (244, 40, 50, 50, 76), (34, 252, 60, 46, 50), (250, 250, 50, 50, 66)]
    boxes = box(*dc, 0.04) + "".join(box(*b, round(0.18 + i * 0.04, 2)) for i, b in enumerate(blds))
    cx, cy = 170, 170
    centers = [(b[0] + b[2] / 2, b[1] + b[3] / 2) for b in blds]
    edges = [(cx, cy, x, y, round(0.36 + i * 0.03, 2), True) for i, (x, y) in enumerate(centers)]
    cams = [(118, 300), (306, 168), (168, 26)]
    edges += [(64, 274, 118, 300, 0.56, False), (269, 65, 306, 168, 0.59, False), (64, 58, 168, 26, 0.62, False)]
    ring = [centers[0], centers[1], centers[3], centers[2], centers[0]]
    edges += [(*ring[i], *ring[i + 1], round(0.72 + i * 0.03, 2), True) for i in range(4)]
    plane = f'<div class="iso-plane">{ground(edges, [])}</div>'
    cam = "".join(pillar(x, y, 30, round(0.6 + i * 0.03, 2)) for i, (x, y) in enumerate(cams))
    tags = (tag(170, 170, 128, 0.1, "Centro de datos") + tag(*centers[1], 92, 0.3, "Sedes")
            + tag(306, 168, 44, 0.64, "Videovigilancia") + tag(*centers[2], 66, 0.78, "Redundancia"))
    return scene(plane + boxes + cam + tags)


# ---------------------------------------------------------------- page sections

def story_section(sid, eyebrow, message, caps, scene_html, gap=58):
    caps_html = "".join(f'<li data-cap="{t}">{txt}</li>' for t, txt in caps)
    return f"""<section class="story" data-story data-gap="{gap}" aria-labelledby="{sid}">
  <div class="story__stage">
    <div class="container story__inner">
      <div class="story__text">
        <p class="eyebrow">{eyebrow}</p>
        <h2 id="{sid}">{message}</h2>
        <ol class="story__caps">{caps_html}</ol>
        <div class="story__progress" aria-hidden="true"><span></span></div>
      </div>
      {scene_html}
    </div>
  </div>
</section>
"""


def features_section(fid, eyebrow, title, lead, items, cols="grid--3", extra_card=""):
    cards = "".join(
        f"""<article class="card tilt feature">
        <span class="feature__num">{i:02d}</span>
        <h3>{h}</h3>
        <p>{p}</p>
      </article>""" for i, (h, p) in enumerate(items, 1))
    return f"""<section class="section" id="capacidades" aria-labelledby="{fid}">
  <div class="container">
    <div class="section__head">
      <p class="eyebrow">{eyebrow}</p>
      {kin(title, "h2", attrs=f' id="{fid}"')}
    </div>
    <div class="grid {cols}" data-stagger>
      {cards}{extra_card}
    </div>
  </div>
</section>
"""


def related_section(slugs, title="Soluciones|*relacionadas*"):
    chips = "".join(f'<li><a class="chip" href="soluciones.html#{s}">{icon(s)}{SVC[s]["name"]}</a></li>' for s in slugs)
    return f"""<section class="section section--alt" aria-labelledby="rel-title">
  <div class="container">
    <div class="section__head">
      <p class="eyebrow">Soluciones</p>
      {kin(title, "h2", attrs=' id="rel-title"')}
      <p class="lead" data-reveal>Cada proyecto combina varias líneas de servicio. Estas son las que más se integran en este sector.</p>
    </div>
    <ul class="chips chips--lg" data-stagger>{chips}</ul>
  </div>
</section>
"""


def build(filename, crumb, title, desc, hero_eyebrow, h1, lead, seed, story, features, related, cta_title, cta_text):
    actions = (f'<div class="btn-row" data-reveal><a class="btn btn--primary magnetic" href="{CTA_HREF}">{CTA_LABEL}{ARROW}</a>'
               f'<a class="btn btn--ghost" href="#capacidades">Ver capacidades</a></div>')
    html = (head(title, desc) + header(filename) + '<main id="contenido">\n'
            + page_hero(hero_eyebrow, h1, lead, crumb, seed, actions)
            + story + features + cta_band(cta_title, cta_text)
            + "</main>\n" + footer(("story.js",)))
    write(filename, html)
