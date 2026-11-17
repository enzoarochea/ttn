from common import *


def empty_art(kind):
    """A lone node with a faint, unfinished network: 'signal waiting'."""
    p = []
    pts = [(40, 60), (50, 160), (170, 40), (200, 170)] if kind == "n" else [(30, 110), (110, 30), (190, 110), (110, 190)]
    c = (110, 110)
    for x, y in pts:
        p.append(edge(*c, x, y, cls="e", thick=1.4))
        p.append(node(x, y, 3.5, extra=' style="opacity:.5"'))
    p.append(f'<circle class="halo" cx="{c[0]}" cy="{c[1]}" r="18"/>')
    p.append(node(*c, 8, cls="n n--hub"))
    return f'<svg class="topo empty__art" viewBox="0 0 220 220" aria-hidden="true" focusable="false">{"".join(p)}</svg>'


def block(sid, eyebrow, title, empty_title, empty_text, kind, actions):
    return f"""<section class="section" id="{sid}" aria-labelledby="{sid}-t">
  <!-- TODO: render {sid} items here when the client starts publishing. Keep this empty state as the fallback when the list is empty. -->
  <div class="container">
    <div class="section__head">
      <p class="eyebrow">{eyebrow}</p>
      {kin(title, "h2", attrs=f' id="{sid}-t"')}
    </div>
    <div class="card empty" data-reveal>
      {empty_art(kind)}
      <div>
        <h3>{empty_title}</h3>
        <p>{empty_text}</p>
        <div class="btn-row">{actions}</div>
      </div>
    </div>
  </div>
</section>
"""


body = f"""<main id="contenido">
{page_hero("Noticias y Eventos", "Noticias|y *eventos*",
           f"Novedades de {BRAND}, proyectos, tecnología y actividades donde puedes encontrarnos.",
           "Noticias y Eventos", 83,
           '<ul class="subnav" data-reveal aria-label="Secciones de la página"><li><a class="chip" href="#noticias">Noticias</a></li><li><a class="chip" href="#eventos">Eventos</a></li></ul>')}
{block("noticias", "Noticias", "Últimas *noticias*", "Todavía no hay noticias publicadas.",
       "Pronto compartiremos aquí novedades sobre proyectos, tecnología y nuestro equipo. Suscríbete al boletín para enterarte primero.",
       "n", f'<a class="btn btn--ghost" href="index.html#boletin">Suscribirme al boletín</a>')}
{fiber()}
{block("eventos", "Eventos", "Próximos *eventos*", "No hay eventos programados por ahora.",
       "Cuando confirmemos charlas, talleres o ferias, los verás aquí con fecha y lugar. Mientras tanto, escríbenos si quieres conversar sobre un proyecto.",
       "e", f'<a class="btn btn--ghost" href="contacto.html">Escríbenos</a>')}
{cta_band()}
</main>
"""
write("noticias-eventos.html", head("Noticias y Eventos", "Noticias, proyectos y eventos de Teltech Networks, S.A. en Guatemala.") + header("noticias-eventos.html") + body + footer())
