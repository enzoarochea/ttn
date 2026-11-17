from common import *
from forms import *

TYPES = [
    ("Asesorías", [("asesoria-tecnologica", "Asesoría tecnológica"), ("asesoria-ciberseguridad", "Asesoría de ciberseguridad"),
                   ("asesoria-ia", "Asesoría de inteligencia artificial"), ("asesoria-herramientas", "Asesoría de herramientas digitales"),
                   ("evaluacion-riesgos", "Evaluación de riesgos de ciberseguridad")]),
    ("Reuniones de descubrimiento", [("descubrimiento-coro", "Coro"), ("descubrimiento-guardz", "Guardz"), ("descubrimiento-searchlight", "Searchlight Cyber"),
                                     ("descubrimiento-ia", "Inteligencia artificial"), ("descubrimiento-kommo", "Kommo CRM")]),
    ("Alianzas", [("partner-red", "Convertirte en partner de red")]),
]
tipo_opts = '<option value="">Selecciona una opción</option>' + "".join(
    f'<optgroup label="{g}">' + "".join(f'<option value="{v}">{label} · 30 min</option>' for v, label in items) + "</optgroup>" for g, items in TYPES)

modes = [("mod-video", "videollamada", "Videollamada"), ("mod-oficina", "presencial", "Presencial en oficina central"), ("mod-tel", "llamada", "Llamada telefónica")]
radios = "".join(
    f'<label class="radio-pill" for="{i}"><input id="{i}" type="radio" name="modalidad" value="{v}" required data-error-id="rs-mod" aria-describedby="rs-mod-error" data-msg-value-missing="Elige cómo prefieres reunirte."><span>{l}</span></label>'
    for i, v, l in modes)

body = f"""<main id="contenido">
{page_hero("Reserva online", "Agenda una|*reunión*",
           "Elige tema, modalidad y fecha. Te confirmamos por correo.",
           "Reserva online", 97, form=True)}
<section class="section" style="padding-top:0" aria-labelledby="reserva-t">
  <div class="container form-wrap">
    <div class="card card--glass" data-reveal>
      <h2 id="reserva-t" style="font-size:var(--fs-h3)">Solicitud de reunión</h2>
      <!-- TODO: booking submission endpoint (data-endpoint) pending client decision. No calendar integration by design. -->
      <form class="form" data-form data-success="reserva-ok" data-endpoint="TODO-booking-endpoint" novalidate>
        {field("rs-tipo", "tipo", "Tipo de reunión", kind="select", placeholder=tipo_opts, attrs=' data-msg-value-missing="Elige el tipo de reunión."')}
        <div class="form__row form__row--2">
          {field("rs-nombre", "nombre", "Nombre completo", autocomplete="name")}
          {field("rs-empresa", "empresa", "Empresa o institución", autocomplete="organization")}
        </div>
        <div class="form__row form__row--2">
          {field("rs-correo", "correo", "Correo electrónico", kind="email", autocomplete="email", placeholder="nombre@empresa.com", attrs=EMAIL_MSG)}
          {field("rs-tel", "telefono", "Teléfono", kind="tel", autocomplete="tel", placeholder="+502 5555 5555", attrs=PHONE_ATTRS)}
        </div>
        <fieldset class="field">
          <legend>Modalidad</legend>
          <div class="radio-row">{radios}</div>
          <p class="field__error" id="rs-mod-error" aria-live="polite"></p>
        </fieldset>
        <div class="form__row form__row--2">
          {field("rs-fecha", "fecha", "Fecha preferida", kind="date", attrs=' data-min-today data-msg-range-underflow="Elige una fecha a partir de hoy."')}
          {field("rs-franja", "franja", "Horario preferido", kind="select", placeholder='<option value="">Selecciona una opción</option><option value="manana">Mañana (8:00 a 12:00)</option><option value="tarde">Tarde (12:00 a 17:00)</option>', attrs=' data-msg-value-missing="Elige un horario."')}
        </div>
        {field("rs-comentarios", "comentarios", "¿Qué te gustaría conversar?", kind="textarea", required=False, placeholder="Cuéntanos brevemente el contexto de tu proyecto.")}
        {consent("rs-consent", f"Acepto que {BRAND} use estos datos únicamente para coordinar la reunión.")}
        {honeypot("rs-web")}
        <p class="form__status" role="alert"></p>
        <button class="btn btn--primary magnetic" type="submit">Enviar solicitud{ARROW}</button>
        <p class="form__note">La fecha queda sujeta a confirmación. {HOURS}.</p>
      </form>
      <div class="form-success" id="reserva-ok" hidden>
        {icon("calendar", "icon form-success__icon")}
        <h3>Solicitud recibida</h3>
        <p>Gracias. Revisaremos la disponibilidad y te contactaremos para confirmar la fecha y la hora de la reunión.</p>
        <button class="btn btn--ghost btn--sm" type="button" data-form-reset>Enviar otra solicitud</button>
      </div>
    </div>
  </div>
</section>
</main>
"""
write("reserva.html", head("Reserva online", "Agenda una reunión de 30 minutos con Teltech Networks, S.A.: asesorías, reuniones de descubrimiento o alianzas, por videollamada, llamada o en la oficina central.") + header("reserva.html") + body + footer())
