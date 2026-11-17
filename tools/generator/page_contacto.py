from common import *
from forms import *
from services import service_options


def map_svg():
    """Abstract street-grid placeholder with a pulsing location node. Not a real map."""
    p = []
    for x in range(-40, 700, 70):
        p.append(edge(x, -20, x + 120, 420, cls="e", thick=1))
    for y in range(10, 420, 60):
        p.append(edge(-20, y, 700, y - 60, cls="e", thick=1))
    p.append('<circle class="halo" cx="330" cy="170" r="22"/>')
    p.append(node(330, 170, 8, cls="n n--hub"))
    return f'<svg class="topo topo--draw" viewBox="0 0 640 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">{"".join(p)}</svg>'


addr = "<br>".join(ADDRESS_LINES)
vert_opts = ('<option value="">Selecciona una opción</option><option value="telcos">Telcos e ISP</option>'
             '<option value="empresas">Empresas</option><option value="gobierno">Gobierno</option><option value="otro">Otro</option>')

body = f"""<main id="contenido">
{page_hero("Contacto", "Hablemos de|tu *proyecto*",
           "Escríbenos o solicita una cotización.",
           "Contacto", 109, form=True)}
<section class="section" style="padding-top:0" aria-label="Datos de contacto y formulario">
  <div class="container contact-grid">
    <div data-reveal>
      <h2 style="font-size:var(--fs-h3)">Datos de contacto</h2>
      <ul class="contact-list">
        <li><span class="ci">{icon("pin")}</span><div><strong>Dirección</strong><address>{addr}</address></div></li>
        <li><span class="ci">{icon("phone")}</span><div><strong>PBX</strong><a href="tel:{PBX_TEL}">{PBX_DISPLAY}</a></div></li>
        <li><span class="ci">{icon("mail")}</span><div><strong>Correo</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
        <li><span class="ci">{icon("clock")}</span><div><strong>Horario</strong>{HOURS}</div></li>
      </ul>
      <!-- TODO: replace this placeholder with the approved map embed (e.g. an <iframe loading="lazy" title="Mapa de ubicación">) once the client confirms the provider. -->
      <div class="card map-ph" role="img" aria-label="Ubicación: 19 Avenida “A” 4-52, Zona 15, Vista Hermosa I, Ciudad de Guatemala">
        {map_svg()}
        <p class="map-ph__label">Oficina central · Vista Hermosa I, Zona 15<span>Ciudad de Guatemala</span></p>
      </div>
      <p class="form__note" style="margin-top:1.5rem">¿Prefieres conversar primero? <a class="link-arrow" href="reserva.html"><span>Agenda una reunión</span>{ARROW}</a></p>
    </div>
    <div class="card card--glass" id="cotizacion" data-reveal>
      <h2 style="font-size:var(--fs-h3)">Solicitar cotización</h2>
      <!-- TODO: contact/quote submission endpoint (data-endpoint) pending client decision. -->
      <form class="form" data-form data-success="contacto-ok" data-endpoint="TODO-contact-endpoint" novalidate>
        <div class="form__row form__row--2">
          {field("ct-nombre", "nombre", "Nombre completo", autocomplete="name")}
          {field("ct-empresa", "empresa", "Empresa o institución", autocomplete="organization")}
        </div>
        <div class="form__row form__row--2">
          {field("ct-correo", "correo", "Correo electrónico", kind="email", autocomplete="email", placeholder="nombre@empresa.com", attrs=EMAIL_MSG)}
          {field("ct-tel", "telefono", "Teléfono", kind="tel", required=False, autocomplete="tel", placeholder="+502 5555 5555", attrs=PHONE_ATTRS)}
        </div>
        {field("ct-servicio", "servicio", "Servicio de interés", kind="select", placeholder=service_options(), attrs=' data-msg-value-missing="Elige un servicio o «Otro»."')}
        {field("ct-mensaje", "mensaje", "Cuéntanos sobre tu proyecto", kind="textarea", placeholder="Alcance, ubicación, plazos y cualquier detalle que nos ayude a preparar la propuesta.", attrs=' minlength="20" data-msg-too-short="Agrega un poco más de detalle (al menos 20 caracteres)."')}
        {consent("ct-consent", f"Acepto que {BRAND} use estos datos únicamente para responder a mi solicitud.")}
        {honeypot("ct-web")}
        <p class="form__status" role="alert"></p>
        <button class="btn btn--primary magnetic" type="submit">{CTA_LABEL}{ARROW}</button>
      </form>
      <div class="form-success" id="contacto-ok" hidden>
        {icon("check-circle", "icon form-success__icon")}
        <h3>Solicitud enviada</h3>
        <p>Gracias por escribirnos. Revisaremos tu solicitud y te contactaremos con los siguientes pasos.</p>
        <button class="btn btn--ghost btn--sm" type="button" data-form-reset>Enviar otra solicitud</button>
      </div>
    </div>
  </div>
</section>
</main>
"""
write("contacto.html", head("Contacto", "Contacta a Teltech Networks, S.A.: 19 Avenida “A” 4-52, Zona 15, Vista Hermosa I, Ciudad de Guatemala. PBX +502 2231 3400.") + header("contacto.html") + body + footer())
