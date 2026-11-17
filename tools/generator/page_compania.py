import json
import math
from common import *

PENDING = '<p class="pending">Pendiente: contenido del cliente</p>'
AVATAR = ('<svg class="ph__avatar" viewBox="0 0 72 72" aria-hidden="true" focusable="false">'
          '<circle cx="36" cy="36" r="34" fill="none" stroke="var(--c-base-600)" stroke-width="1.5" stroke-dasharray="4 5"/>'
          '<circle cx="36" cy="28" r="9" fill="var(--c-neutral-400)" opacity=".35"/><path d="M18 56c3-10 10-15 18-15s15 5 18 15" fill="none" stroke="var(--c-neutral-400)" stroke-width="2" opacity=".4"/></svg>')
BARS = '<div class="ph__bar ph__bar--l"></div><div class="ph__bar ph__bar--m"></div><div class="ph__bar ph__bar--s"></div>'


def region_map():
    """Flat dot map of Central America + Florida from the globe dataset."""
    geo = json.load(open(GEO))
    lon0, lon1, lat0, lat1 = -94.5, -77.0, 7.0, 28.5
    W = 640
    kx = W / (lon1 - lon0)
    ky = kx / math.cos(math.radians(17))
    H = round((lat1 - lat0) * ky)
    P = lambda lat, lon: ((lon - lon0) * kx, (lat1 - lat) * ky)
    land, hot = [], []
    for lat, lon, f in geo["dots"]:
        if lon0 <= lon <= lon1 and lat0 <= lat <= lat1:
            x, y = P(lat, lon)
            (hot if f == 1 else land).append(f"M{x:.0f} {y:.0f}h0")
    cities = [(n, la, lo, hq, dx, dy, anc) for n, la, lo, hq, dx, dy, anc in [
        ("Ciudad de Guatemala", 14.6349, -90.5069, True, -10, -14, "end"), ("El Salvador", 13.6929, -89.2182, False, -6, 22, "end"),
        ("Nicaragua", 12.1364, -86.2514, False, 12, 4, "start"), ("Costa Rica", 9.9281, -84.0907, False, 12, 4, "start"), ("Miami", 25.7617, -80.1918, False, 12, 4, "start")]]
    gx, gy = P(cities[0][1], cities[0][2])
    arcs, marks = [], []
    for name, la, lo, hq, dx, dy, anc in cities:
        x, y = P(la, lo)
        if not hq:
            mx, my = (gx + x) / 2, (gy + y) / 2 - math.hypot(x - gx, y - gy) * 0.28
            arcs.append(f'<path class="arc" d="M{gx:.1f} {gy:.1f}Q{mx:.1f} {my:.1f} {x:.1f} {y:.1f}"/>')
        r = 6 if hq else 4.5
        marks.append(f'<circle class="city-ring" cx="{x:.1f}" cy="{y:.1f}" r="{r + 6}"/><circle class="city" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
                     f'<text class="city-lbl" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anc}">{name}</text>')
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Mapa de presencia: sede central en Ciudad de Guatemala y operación en El Salvador, Nicaragua, Costa Rica y Miami.">'
            f'<path class="land-dots" d="{"".join(land)}"/><path class="land-dots land-dots--hot" d="{"".join(hot)}"/>'
            f'{"".join(arcs)}{"".join(marks)}</svg>')


def section(sid, eyebrow, title, note, inner, alt=False, pending=True):
    comment = f"<!-- PENDING CLIENT CONTENT: {title}. Replace placeholders once the client supplies verified content. -->" if pending else ""
    return f"""<section class="section{' section--alt' if alt else ''}" id="{sid}" aria-labelledby="{sid}-t">
  {comment}
  <div class="container">
    <div class="section__head">
      <p class="eyebrow">{eyebrow}</p>
      {kin(title, "h2", attrs=f' id="{sid}-t"')}
      {PENDING if pending else ""}
      <p class="muted" data-reveal>{note}</p>
    </div>
    {inner}
  </div>
</section>
"""


region_list = "".join(f'<li><b>{n}</b><span>{d}</span></li>' for n, d in [
    ("Guatemala", "Sede central · Ciudad de Guatemala"), ("El Salvador", "Operación"), ("Nicaragua", "Operación"), ("Costa Rica", "Operación"), ("Miami", "Operación · Estados Unidos")])
region = f"""<div class="region">
      <div class="card region__map" data-reveal>{region_map()}</div>
      <div data-reveal>
        <ul class="region__list">{region_list}</ul>
        <ul class="contact-list" style="margin-top:2rem">
          <li><span class="ci">{icon("pin")}</span><div><strong>Oficina central</strong><address>{"<br>".join(ADDRESS_LINES)}</address></div></li>
          <li><span class="ci">{icon("clock")}</span><div><strong>Horario</strong>{HOURS}</div></li>
        </ul>
      </div>
    </div>"""

timeline = f"""<ol class="timeline" data-stagger>
      <li><div class="card"><span class="timeline__year">2013</span><h3>Fundación en Ciudad de Guatemala</h3><p class="muted" style="margin:0">Nace {BRAND} con operación central en la capital guatemalteca.</p></div></li>
      <li><div class="card ph" aria-hidden="true"><p class="sol__label">Hito por confirmar</p>{BARS}</div></li>
      <li><div class="card ph" aria-hidden="true"><p class="sol__label">Hito por confirmar</p>{BARS}</div></li>
      <li><div class="card"><span class="timeline__year">Hoy</span><h3>Cinco puntos de operación</h3><p class="muted" style="margin:0">Guatemala, El Salvador, Nicaragua, Costa Rica y Miami.</p></div></li>
    </ol>"""
team = '<div class="grid grid--4" data-stagger>' + "".join(f'<div class="card ph" aria-hidden="true">{AVATAR}<div class="ph__bar ph__bar--m"></div><div class="ph__bar ph__bar--s"></div></div>' for _ in range(4)) + "</div>"
certs = '<div class="grid grid--3" data-stagger>' + "".join(f'<div class="card ph" aria-hidden="true"><span class="sol__icon" style="margin-bottom:1rem">{icon("check-circle")}</span><div class="ph__bar ph__bar--m"></div><div class="ph__bar ph__bar--s"></div></div>' for _ in range(3)) + "</div>"
values = '<div class="grid grid--4" data-stagger>' + "".join(f'<div class="card ph" aria-hidden="true"><span class="feature__num">0{i}</span><div class="ph__bar ph__bar--m"></div>{BARS}</div>' for i in range(1, 5)) + "</div>"

body = f"""<main id="contenido">
{page_hero("Compañía", "Conectamos la región|*desde 2013*",
           f"{BRAND} fue fundada en 2013 con sede central en Ciudad de Guatemala y hoy opera también en El Salvador, Nicaragua, Costa Rica y Miami, comprometida con la innovación y la excelencia en cada proyecto.",
           "Compañía", 71, '<div class="btn-row" data-reveal><a class="btn btn--ghost" href="soluciones.html">Conoce nuestras soluciones</a></div>')}
<section class="section section--tight" aria-label="Cifras">
  <div class="container">
    <ul class="stats" data-reveal>
      <li class="stat"><span class="stat__num" data-count="2013" data-from="2000">2013</span><span class="stat__label">Año de fundación</span></li>
      <li class="stat"><span class="stat__num" data-count="5">5</span><span class="stat__label">Puntos de operación</span></li>
      <li class="stat"><span class="stat__num" data-count="4">4</span><span class="stat__label">Países con operación</span></li>
      <li class="stat"><span class="stat__num" data-count="13">13</span><span class="stat__label">Soluciones integradas</span></li>
    </ul>
  </div>
</section>
{section("presencia", "Presencia", "Una red,|cinco puntos de *operación*", "Sede central en Guatemala y operación en Centroamérica y Estados Unidos.", region, pending=False)}
{section("historia", "Historia", "Nuestra *historia*", "Los hitos intermedios se publicarán cuando la empresa los confirme.", timeline, alt=True)}
{section("equipo", "Equipo", "El *equipo*", "Aquí se presentará al equipo directivo y técnico con información aprobada por la empresa.", team)}
{section("certificaciones", "Certificaciones", "Certificaciones y|*acreditaciones*", "Solo se publicarán certificaciones vigentes y verificadas por la empresa.", certs, alt=True)}
{section("valores", "Valores", "Nuestros *valores*", "Los valores se publicarán con la redacción que defina la empresa.", values)}
{cta_band()}
</main>
"""
write("compania.html", head("Compañía", "Teltech Networks, S.A.: fundada en 2013, con sede central en Ciudad de Guatemala y operación en El Salvador, Nicaragua, Costa Rica y Miami.") + header("compania.html") + body + footer())
