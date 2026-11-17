from vertical import *

story = story_section(
    "story-gobierno", "Gobierno",
    "Infraestructura pública con orden, trazabilidad y cumplimiento.",
    [(0.0, "Centros de datos que concentran y resguardan la información institucional."),
     (0.3, "Sedes y videovigilancia conectadas a una misma red."),
     (0.66, "Enlaces redundantes y procesos digitalizados que dejan registro de cada paso.")],
    scene_gobierno())

cta_card = f"""<article class="card feature feature--cta">
        <div>
          <span class="feature__num">¿Tienes unas bases?</span>
          <h3>Revisemos tu proyecto de licitación</h3>
          <p>Compártenos el alcance técnico y te ayudamos a preparar una propuesta completa.</p>
        </div>
        <a class="link-arrow" href="{CTA_HREF}"><span>{CTA_LABEL}</span>{ARROW}</a>
      </article>"""

features = features_section(
    "cap-gobierno", "Capacidades",
    "Proyectos públicos,|ejecutados con *rigor.*",
    "Diseñamos soluciones para instituciones públicas alineadas con marcos normativos, procesos de contratación y altos estándares de transparencia, para modernizar la gestión y mejorar el servicio al ciudadano.",
    [
        ("Proyectos de licitación", "Ejecución bajo esquemas de licitación, con gestión de proyectos complejos de principio a fin."),
        ("Cumplimiento regulatorio", "Diseños y documentación alineados con la normativa aplicable a cada institución."),
        ("Centros de datos", "Diseño, adecuación y equipamiento de centros de datos y cuartos de comunicaciones."),
        ("Videovigilancia", "Sistemas de video, analítica y centros de monitoreo para edificios y espacios públicos."),
        ("Digitalización de procesos", "Trámites y archivos digitales con trazabilidad, seguridad y control de acceso."),
        ("Telecomunicaciones y ciberseguridad", "Conectividad entre sedes y protección de la información institucional."),
    ],
    extra_card="")

features = features.replace("{cards}{extra_card}", "")  # no-op safety
features = features.replace("</div>\n  </div>\n</section>", f"{cta_card}\n    </div>\n  </div>\n</section>", 1)

related = related_section(["infraestructura-ti", "seguridad", "ciberseguridad", "redes", "automatizacion-procesos", "negocios-web", "asesoria-consultoria", "servicios-administrados"])

build("gobierno.html", "Gobierno", "Gobierno",
      "Proyectos de licitación, cumplimiento regulatorio, centros de datos, videovigilancia y digitalización para instituciones de gobierno.",
      "Vertical · Gobiernos e instituciones",
      "Tecnología pública|que rinde *cuentas*",
      "Desarrollamos proyectos de infraestructura tecnológica, telecomunicaciones, ciberseguridad, centros de datos, videovigilancia y digitalización que fortalecen la seguridad y la transformación digital de las instituciones.",
      37, story, features, related,
      "¿Preparas una licitación|de *tecnología?*",
      "Conversemos sobre el alcance técnico de tu proyecto y cómo podemos apoyarte desde la propuesta.")
