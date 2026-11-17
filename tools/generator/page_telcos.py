from vertical import *

story = story_section(
    "story-telcos", "Telcos e ISP",
    "De la central a la última milla.",
    [(0.0, "Planta interna y transmisión."),
     (0.3, "Fibra óptica y GPON hasta el cliente."),
     (0.6, "Enlaces inalámbricos en zonas rurales.")],
    scene_telcos())

features = features_section(
    "cap-telcos", "Capacidades",
    "Lo que construimos|para *operadores.*", "",
    [
        ("Fibra óptica y GPON", "Tendido, empalmes y redes ópticas pasivas."),
        ("Enlaces inalámbricos", "Punto a punto, multipunto y microondas."),
        ("Última milla", "Instalación y activación hasta el cliente."),
        ("Planta interna y externa", "Centrales, nodos, postes y ductos."),
        ("Transmisión y RF", "Transporte entre nodos y sistemas de radio."),
        ("Sitios y zonas rurales", "Montaje, desmontaje y expansión de cobertura."),
    ])

build("telcos-isp.html", "Telcos e ISP", "Telcos e ISP",
      "Construcción de red, fibra óptica, GPON, enlaces inalámbricos y despliegue de última milla para operadores e ISP.",
      "Vertical · Telcos e ISP",
      "Red para|*operadores*",
      "Infraestructura de red y despliegue de última milla para que operadores e ISP crezcan.",
      11, story, features, "",
      "¿Planeas ampliar|tu *red?*",
      "Cuéntanos el alcance y preparamos una propuesta técnica.")
