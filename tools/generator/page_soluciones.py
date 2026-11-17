from common import *
from services import GRID, EXTRA


def card(i, s):
    items = [it for _, g in s["groups"] for it in g][:4]
    chips = "".join(f'<li class="chip">{it}</li>' for it in items)
    return f"""<article class="card tilt solc" id="{s['slug']}" aria-labelledby="{s['slug']}-t">
        <div class="solc__head">
          <span class="sol__icon">{icon(s['slug'])}</span>
          <div><span class="sol__num">{i:02d}</span><h3 id="{s['slug']}-t">{s['name']}</h3></div>
        </div>
        <p>{s['short']}</p>
        <ul class="chips" aria-label="Incluye">{chips}</ul>
        <a class="link-arrow" href="contacto.html?servicio={s['slug']}#cotizacion"><span>Cotizar</span>{ARROW}</a>
      </article>"""


body = f"""<main id="contenido">
{page_hero("Soluciones", "Soluciones que conectan,|protegen y *automatizan*",
           "Servicios diseñados para integrarse entre sí.", "Soluciones", 53)}
<section class="section" style="padding-top:0" aria-label="Catálogo de soluciones">
  <div class="container">
    <h2 class="sol-group-title">Ecosistema tecnológico</h2>
    <div class="sol-grid" data-stagger>{''.join(card(i, s) for i, s in enumerate(GRID, 1))}</div>
    <h2 class="sol-group-title">Servicios especializados</h2>
    <div class="sol-grid" data-stagger>{''.join(card(i, s) for i, s in enumerate(EXTRA, len(GRID) + 1))}</div>
  </div>
</section>
{cta_band("¿No sabes por dónde|*empezar?*", "Te recomendamos la combinación ideal para tu operación.")}
</main>
"""
write("soluciones.html", head("Soluciones", "Telecomunicaciones, redes, infraestructura TI, seguridad, ciberseguridad, comunicaciones, audio y video, servicios administrados, automatización e IA.") + header("soluciones.html") + body + footer())
