from vertical import *

story = story_section(
    "story-empresas", "Empresas",
    "Una sola arquitectura para toda la operación.",
    [(0.0, "Infraestructura y redes a tu medida."),
     (0.3, "Seguridad y comunicaciones sobre la misma base."),
     (0.62, "Automatización e IA operando como un sistema.")],
    scene_empresas())

features = features_section(
    "cap-empresas", "Capacidades",
    "Todo integrado,|en un solo *diseño.*", "",
    [
        ("Infraestructura TI", "Centros de datos, servidores y almacenamiento."),
        ("Redes", "WiFi, cableado estructurado y fibra."),
        ("Ciberseguridad", "Dispositivos, correo, datos y red."),
        ("Comunicaciones unificadas", "Telefonía IP, colaboración y contact center."),
        ("Automatización", "RPA, flujos de trabajo e inteligencia artificial."),
        ("Servicios administrados", "Operación y soporte bajo acuerdos de servicio."),
    ])

build("empresas.html", "Empresas", "Empresas",
      "Arquitecturas tecnológicas integrales para medianas y grandes empresas.",
      "Vertical · Empresas",
      "Tecnología que trabaja|como un solo *sistema*",
      "Integramos TI, redes, seguridad y automatización para medianas y grandes empresas.",
      23, story, features, "",
      "¿Tu tecnología creció|*por partes?*",
      "Revisemos tu arquitectura y la integramos en un solo diseño.")
