import random
import sys
from common import *
from services import GRID, VERTICALS

BASE_ONLY = "--base" in sys.argv


def mini(kind):
    """Small topology per vertical, shown on a tilted isometric plane."""
    p = []
    if kind == "telcos":
        root = (12, 40)
        p.append(edge(*root, 52, 40, cls="e e--hot", pulse=True, d=0, thick=2))
        for y in (14, 40, 66):
            p.append(edge(52, 40, 92, y, pulse=(y == 14), d=400))
            p.append(edge(92, y, 112, y, d=700))
            p.append(node(112, y, 2.6)); p.append(node(92, y, 2.2))
        p.append(node(52, 40, 3.4)); p.append(node(*root, 4.4, cls="n n--hub"))
    elif kind == "empresas":
        c = (62, 40)
        pts = [(22, 12), (102, 12), (114, 44), (88, 70), (34, 70), (10, 42)]
        for i, q in enumerate(pts):
            p.append(edge(*c, *q, cls="e e--hot" if i % 2 == 0 else "e", pulse=i in (0, 3), d=i * 200, thick=1.8))
        for i in range(len(pts)):
            p.append(edge(*pts[i], *pts[(i + 1) % len(pts)], d=900))
        for q in pts:
            p.append(node(*q, 2.6))
        p.append(node(*c, 4.6, cls="n n--hub"))
    else:
        xs, ys = (16, 62, 108), (12, 40, 68)
        for y in ys:
            p.append(edge(xs[0], y, xs[2], y, pulse=(y == 40), d=200))
        for x in xs:
            p.append(edge(x, ys[0], x, ys[2], cls="e e--hot" if x == 62 else "e", d=500, thick=2 if x == 62 else 1.6))
        for x in xs:
            for y in ys:
                hub = (x, y) == (62, 12)
                p.append(node(x, y, 4.2 if hub else 2.4, cls="n n--hub" if hub else "n"))
    return f'<div class="isoflat"><svg class="topo" viewBox="0 0 124 80" aria-hidden="true" focusable="false">{"".join(p)}</svg></div>'


locs = "".join(
    f'<li data-loc="{lid}"{" class=\"hq\"" if hq else ""}>{name}</li>' for lid, name, hq in LOCATIONS)
specialties = ["Telecomunicaciones", "Infraestructura", "Ciberseguridad", "Automatización", "Inteligencia artificial"]

hero = f"""<main id="contenido">
<section class="hero" data-hero aria-labelledby="hero-title">
  <div class="hero__globe" aria-hidden="true">
    {globe_static_svg("d")}
    {globe_static_svg("m")}
    <canvas class="hero__canvas"></canvas>
  </div>
  <div class="container hero__content">
    <p class="eyebrow" data-seq>Integrador de soluciones tecnológicas · Desde 2013</p>
    {kin("Conectamos|la *región.*", attrs=' id="hero-title" data-kin-auto')}
    <p class="lead" data-seq style="--sd:250ms">Telecomunicaciones, infraestructura, ciberseguridad y automatización para operadores y empresas.</p>
    <div class="btn-row" data-seq style="--sd:380ms">
      <a class="btn btn--primary magnetic" href="{CTA_HREF}">{CTA_LABEL}{ARROW}</a>
      <a class="btn btn--ghost" href="soluciones.html">Ver soluciones</a>
    </div>
    <div class="hero__foot" data-seq style="--sd:520ms">
      <ul class="locs" aria-label="Puntos de operación">{locs}</ul>
      <a class="scroll-cue" href="#cifras"><span class="scroll-cue__line" aria-hidden="true"></span>Desplázate</a>
    </div>
  </div>
</section>
"""

stats = [("2013", "2000", "Año de fundación", ""), ("5", "0", "Puntos de operación", ""), ("13", "0", "Soluciones integradas", "")]
stats_html = "".join(
    f'<li class="stat"><span class="stat__num" data-count="{n}" data-from="{f}">{n}</span><span class="stat__label">{lbl}</span></li>' for n, f, lbl, _ in stats)


def signal(i):
    """Small animated signal path, different per panel."""
    rnd = random.Random(i * 7)
    xs = [8, 70, 140, 210, 282]
    ys = [rnd.randint(10, 46) for _ in xs]
    parts = []
    for k in range(len(xs) - 1):
        parts.append(edge(xs[k], ys[k], xs[k + 1], ys[k + 1], cls="e e--hot" if k == 0 else "e", pulse=k in (0, 2), d=k * 300, thick=1.6))
    for k, (x, y) in enumerate(zip(xs, ys)):
        parts.append(node(x, y, 4 if k == 0 else 2.6, cls="n n--hub" if k == 0 else "n"))
    return f'<div class="eco__viz" aria-hidden="true"><svg class="topo" viewBox="0 0 290 56" preserveAspectRatio="none">{"".join(parts)}</svg></div>'


def eco(i, s):
    return f"""<a class="eco" href="soluciones.html#{s['slug']}">
        <span class="eco__num" aria-hidden="true">{i:02d}</span>
        <span class="eco__icon">{icon(s['slug'])}</span>
        <h3>{s['name']}</h3>
        <p>{s['short']}</p>
        {signal(i)}
        <span class="eco__more">Ver detalle{ARROW}</span>
      </a>"""


vtext = {
    "telcos": ("01", "Red de acceso y transporte, fibra, GPON y última milla para operadores e ISP.", "Explorar Telcos e ISP"),
    "empresas": ("02", "TI, redes, ciberseguridad y comunicaciones integradas en una sola arquitectura.", "Explorar Empresas"),
}
vpanels = "".join(
    f"""<a class="card tilt vpanel" href="{VERTICALS[k][1]}">
      <span class="vpanel__index">{n} / Vertical</span>
      <div class="vpanel__scene" aria-hidden="true">{mini(k)}</div>
      <h3>{VERTICALS[k][0]}</h3>
      <p>{txt}</p>
      <span class="link-arrow"><span>{cta}</span>{ARROW}</span>
    </a>""" for k, (n, txt, cta) in vtext.items())

MAKERS = [("hikvision", "Hikvision", 420, 54), ("hanwha", "Hanwha", 354, 96), ("cambium", "Cambium Networks", 326, 96), ("mitel", "Mitel", 408, 96),
          ("hpe", "Hewlett Packard Enterprise", 230, 96), ("zoom", "Zoom", 105, 96), ("optoma", "Optoma", 317, 96), ("ezviz", "EZVIZ", 310, 96), ("ruijie", "Ruijie", 307, 96)]
makers = "".join(
    f'<li class="logo-tile"><img src="img/partners/{s}.webp" alt="{n}" width="{w}" height="{h}" loading="lazy" decoding="async" style="aspect-ratio:{w}/{h}"></li>' for s, n, w, h in MAKERS)
ECO = [("Searchlight Cyber", "Ciberseguridad"), ("Coro", "Ciberseguridad"), ("Guardz", "Ciberseguridad"), ("BornDigitalIA", "Inteligencia artificial")]
eco_partners = "".join(f'<li class="logo-tile logo-tile--word">{n}<span>{c}</span></li>' for n, c in ECO)

body = f"""<section class="section section--tight" id="cifras" aria-label="Cifras">
  <div class="container">
    <ul class="stats" data-reveal>{stats_html}</ul>
  </div>
</section>
<section class="htrack" data-htrack aria-labelledby="eco-title">
  <div class="htrack__sticky">
    <div class="container htrack__head">
      <div>
        <p class="eyebrow">Ecosistema tecnológico</p>
        {kin("Nueve líneas.|Un solo *sistema.*", "h2", attrs=' id="eco-title"')}
      </div>
      <p class="htrack__count" aria-hidden="true"><b data-htrack-current>01</b> / {len(GRID):02d}</p>
    </div>
    <div class="htrack__rail">
      {"".join(eco(i, s) for i, s in enumerate(GRID, 1))}
    </div>
    <div class="htrack__bar" aria-hidden="true"><span></span></div>
  </div>
</section>
<section class="section" id="verticales" aria-labelledby="verticales-title">
  <div class="container">
    <div class="section__head">
      <p class="eyebrow">Verticales</p>
      {kin("Hecho para|tu *sector.*", "h2", attrs=' id="verticales-title"')}
    </div>
    <div class="grid grid--2" data-stagger>
      {vpanels}
    </div>
  </div>
</section>
<section class="section" id="aliados" aria-labelledby="aliados-title">
  <div class="container">
    <div class="section__head">
      <p class="eyebrow">Aliados</p>
      {kin("Tecnología|que *integramos.*", "h2", attrs=' id="aliados-title"')}
    </div>
  </div>
  <div class="marquee" style="--mq:60s"><ul class="marquee__track" aria-label="Fabricantes y aliados">{makers}{eco_partners}</ul></div>
</section>
<section class="section" id="boletin" aria-labelledby="boletin-title">
  <div class="container">
    <div class="card card--glass newsletter" data-reveal>
      <div>
        <p class="eyebrow">Boletín</p>
        <h2 id="boletin-title" style="font-size:clamp(1.5rem,1.1rem + 1.6vw,2.6rem)">Novedades y eventos, en tu correo.</h2>
      </div>
      <div>
        <!-- TODO: newsletter submission endpoint (data-endpoint) pending client decision. -->
        <form class="form" data-form data-success="boletin-ok" data-endpoint="TODO-newsletter-endpoint" novalidate>
          <div class="form__inline">
            <div class="field">
              <label for="nl-email">Correo electrónico</label>
              <input id="nl-email" name="correo" type="email" autocomplete="email" required placeholder="nombre@empresa.com" aria-describedby="nl-email-error" data-msg-type-mismatch="Escribe un correo válido, por ejemplo nombre@empresa.com.">
              <p class="field__error" id="nl-email-error" aria-live="polite"></p>
            </div>
            <button class="btn btn--primary" type="submit">Suscribirme</button>
          </div>
          <div class="field" style="margin-top:0.75rem">
            <label class="check" for="nl-consent"><input id="nl-consent" name="consentimiento" type="checkbox" required aria-describedby="nl-consent-error" data-msg-value-missing="Confirma que deseas recibir el boletín."><span>Acepto recibir comunicaciones de {BRAND} y sé que puedo darme de baja cuando quiera.</span></label>
            <p class="field__error" id="nl-consent-error" aria-live="polite"></p>
          </div>
          <div class="hp" aria-hidden="true"><label for="nl-web">No completar</label><input id="nl-web" name="web" type="text" tabindex="-1" autocomplete="off"></div>
          <p class="form__status" role="alert"></p>
        </form>
        <div class="form-success" id="boletin-ok" hidden>
          {icon("check-circle", "icon form-success__icon")}
          <h3>¡Listo! Ya estás en la lista.</h3>
          <p>Gracias por suscribirte. Te escribiremos cuando haya novedades.</p>
          <button class="btn btn--ghost btn--sm" type="button" data-form-reset>Suscribir otro correo</button>
        </div>
      </div>
    </div>
  </div>
</section>
{cta_band("¿Listo para|conectar tu *operación?*").replace('class="megacta"', 'class="megacta" data-swarm', 1)}
</main>
"""

desc = "Teltech Networks, S.A.: integrador de telecomunicaciones, infraestructura, ciberseguridad, automatización e inteligencia artificial desde 2013, con sede en Ciudad de Guatemala."
html = head("", desc, intro=True) + header("index.html", intro=True) + (hero + "</main>\n" if BASE_ONLY else hero + body) + footer(("globe-data.js", "globe.js", "swarm.js"))
write("index.html", html)
