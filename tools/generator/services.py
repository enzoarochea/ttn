"""Service catalogue v2. Facts (sub-services) come from the client's current
website; all copy is rewritten. No unconfirmed claims (no round-the-clock service, SOC,
certifications, partner statistics, prices or free offers)."""

VERTICALS = {
    "telcos": ("Telcos e ISP", "telcos-isp.html"),
    "empresas": ("Empresas", "empresas.html"),
    "gobierno": ("Gobierno", "gobierno.html"),
}

GRID = [
    {
        "slug": "telecomunicaciones", "name": "Telecomunicaciones",
        "short": "Planta interna y externa, transmisión, radiofrecuencia y última milla para conectar cualquier entorno.",
        "what": "Construimos y desplegamos la red que sostiene a operadores, empresas e instituciones: desde la central hasta la última milla, también en zonas rurales o de difícil acceso, con infraestructura que reduce tiempos de implementación y costos de operación.",
        "groups": [
            ("Red de operador", ["Planta interna", "Planta externa", "Transmisión (Tx)", "Radiofrecuencia (RF)"]),
            ("Despliegue", ["Instalaciones de última milla", "Montaje de sitios", "Desmontaje de sitios"]),
        ],
        "verticals": ["telcos", "empresas", "gobierno"],
    },
    {
        "slug": "comunicaciones-unificadas", "name": "Comunicaciones Unificadas",
        "short": "Centrales telefónicas, VoIP, colaboración y contact center en una sola plataforma.",
        "what": "Centralizamos y modernizamos la comunicación interna y externa de tu organización para bajar costos de telefonía y mejorar la colaboración de equipos presenciales y remotos.",
        "groups": [
            ("Centrales telefónicas", ["PBX físico", "PBX virtual", "Media gateways", "Terminales telefónicos", "Grabación de llamadas", "Diademas y auriculares"]),
            ("VoIP", ["Teléfonos IP", "Gateways VoIP", "Session Border Controller", "Calidad de servicio (QoS)"]),
            ("Colaboración", ["Softphones", "PBX IP virtual", "Teams, Google Meet y Zoom"]),
            ("Contact center", ["Call center", "Atención omnicanal"]),
        ],
        "verticals": ["empresas", "gobierno"],
    },
    {
        "slug": "infraestructura-ti", "name": "Infraestructura TI",
        "short": "Centros de datos, servidores y almacenamiento para que el negocio no se detenga.",
        "what": "Infraestructura escalable y segura, diseñada para la continuidad del negocio y para responder a una demanda tecnológica que crece todos los días, con menos riesgo de fallas y mejor uso de los recursos.",
        "groups": [
            ("Centro de datos", ["Centros de datos", "Centros de datos autocontenidos", "Servidores", "Almacenamiento"]),
            ("Puesto de trabajo", ["Computadoras", "Impresoras"]),
        ],
        "verticals": ["empresas", "gobierno"],
    },
    {
        "slug": "seguridad", "name": "Seguridad",
        "short": "Videovigilancia, videoanalítica, control de incendios y control de acceso.",
        "what": "Protección integral de personas, instalaciones y activos: sistemas que previenen incidentes, vigilan de forma proactiva y se gestionan desde un mismo centro de monitoreo.",
        "groups": [
            ("Videovigilancia", ["Cámaras", "Software de gestión de video", "Videowalls", "Centros de monitoreo"]),
            ("Videoanalítica", ["Detección de objetos", "Detección de humo y fuego", "Reconocimiento facial", "Uso de casco y chaleco", "Motociclistas sin casco", "Conteo de objetos", "Mapas de calor", "Reconocimiento de placas (LPR)"]),
            ("Control de incendios", ["Detección de incendios", "Supresión de incendios"]),
            ("Control de acceso", ["Videoporteros", "Detectores de metal", "Talanqueras", "Molinetes", "Sistemas de parqueo"]),
        ],
        "verticals": ["empresas", "gobierno"],
    },
    {
        "slug": "redes", "name": "Redes",
        "short": "WiFi, redes de datos, fibra óptica, GPON y enlaces inalámbricos.",
        "what": "Conectividad robusta y confiable, dimensionada para altos volúmenes de tráfico y para que las operaciones críticas funcionen sin interrupciones.",
        "groups": [
            ("WiFi", ["Dimensionamiento", "Diseño de propagación", "Mapas de calor", "Access points", "Gestión de WiFi"]),
            ("Redes de datos", ["LAN switching", "Redes inalámbricas", "Administración de redes", "Monitoreo de servicios y enlaces"]),
            ("Infraestructura física", ["Cableado estructurado", "Fibra óptica", "GPON", "HFC"]),
            ("Enlaces inalámbricos", ["Punto a punto", "Punto a multipunto"]),
        ],
        "verticals": ["empresas", "gobierno", "telcos"],
    },
    {
        "slug": "ciberseguridad", "name": "Ciberseguridad",
        "short": "Protección de dispositivos, correo, datos y red, con análisis predictivo en seguridad.",
        "what": "Ciberseguridad que va más allá del antivirus: prevención, detección y respuesta sobre dispositivos, correo, datos y red, con análisis predictivo en seguridad para anticipar amenazas antes de que afecten la operación.",
        "groups": [
            ("Asesoría", ["Entendimiento del negocio", "Evaluación de riesgos", "Evaluación de vulnerabilidades"]),
            ("Dispositivos", ["Endpoints, servidores y nube", "Agentes para Windows, macOS y Linux", "Firewall, USB y cifrado de discos", "EDR y MDR"]),
            ("Correo electrónico", ["Microsoft 365", "Google Workspace", "Bloqueo de spam, phishing y malware", "Prevención de fuga de información"]),
            ("Datos y red", ["Gobernanza de datos", "Detección de datos sensibles", "SASE y ZTNA", "VPN y filtrado DNS"]),
        ],
        "verticals": ["empresas", "gobierno", "telcos"],
    },
    {
        "slug": "audio-video", "name": "Audio y Video",
        "short": "Videoconferencia, salas colaborativas, pantallas interactivas y aulas inteligentes.",
        "what": "Espacios de colaboración para el trabajo híbrido: salas, auditorios y aulas donde la imagen, el sonido y el control funcionan sin fricción para reuniones y decisiones más efectivas.",
        "groups": [
            ("Videocolaboración", ["Videoconferencia", "Salas colaborativas", "Salas híbridas", "Aulas interactivas e híbridas"]),
            ("Proyección y pantallas", ["Proyectores", "Pantallas interactivas", "Gran formato y LED", "Videowalls"]),
            ("Audio", ["Micrófonos", "Altavoces", "Procesadores de audio (DSP)"]),
            ("Automatización de salas", ["Control centralizado", "Paneles táctiles", "Iluminación y cortinas", "Gestión de salas"]),
        ],
        "verticals": ["empresas", "gobierno"],
    },
    {
        "slug": "servicios-administrados", "name": "Servicios Administrados",
        "short": "Personal especializado, gestión de activos y soluciones como servicio.",
        "what": "Externalizamos con eficiencia servicios tecnológicos estratégicos para que tu equipo se concentre en el negocio, con modelos de servicio flexibles y acuerdos de nivel de servicio definidos contigo.",
        "groups": [
            ("Operación", ["Gestión de personal especializado", "Software de gestión de activos informáticos"]),
            ("Modelos", ["Soluciones XaaS (todo como servicio)", "Acuerdos de nivel de servicio (SLA)"]),
        ],
        "verticals": ["empresas", "gobierno", "telcos"],
    },
    {
        "slug": "automatizacion-procesos", "name": "Automatización de Procesos",
        "short": "RPA, flujos de trabajo, gestión documental y digitalización con inteligencia artificial.",
        "what": "Convertimos procesos manuales y en papel en flujos digitales trazables, y sumamos inteligencia artificial para interpretar datos, automatizar decisiones repetitivas y obtener información útil en tiempo real.",
        "groups": [
            ("Automatización", ["Inteligencia artificial", "RPA y bots", "Flujos de trabajo", "Hiperautomatización"]),
            ("Gestión documental", ["Flujos basados en documentos", "Gestión de documentos digitales", "OCR"]),
            ("Digitalización", ["Digitalización de documentos físicos", "Gestión de metadatos", "Digitalización automatizada"]),
        ],
        "verticals": ["empresas", "gobierno"],
    },
]

EXTRA = [
    {
        "slug": "asesoria-consultoria", "name": "Asesoría y Consultoría",
        "short": "Estrategia tecnológica con acompañamiento de principio a fin.",
        "what": "La tecnología rinde cuando hay estrategia y acompañamiento. Partimos de entender tu negocio y tu industria para trazar una hoja de ruta y servicios configurados a tu tamaño e infraestructura.",
        "groups": [
            ("Método", ["Entendimiento del negocio", "Entendimiento de la industria", "Estrategia y hoja de ruta", "Servicios a la medida"]),
            ("Áreas", ["Riesgos de ciberseguridad", "Comercio digital", "Inteligencia artificial", "Manuales de TI", "Herramientas y procesos", "Modelos operativos de TI e IA", "Automatización", "Asesoría digital 360/365"]),
        ],
        "verticals": ["empresas", "gobierno", "telcos"],
    },
    {
        "slug": "ciberseguridad-monitoreo", "name": "Ciberseguridad y Monitoreo",
        "short": "Seguridad gestionada: detección, respuesta y atención bajo un acuerdo de servicio.",
        "what": "Tú te encargas del negocio y nosotros de tu ciberseguridad: administramos la seguridad con un acuerdo de nivel de servicio que define cómo detectamos, actuamos, respondemos y atendemos cada solicitud.",
        "groups": [
            ("Monitoreo", ["Detección y respuesta (EDR/MDR)", "Monitoreo de la superficie de ataque externa", "Inteligencia de amenazas"]),
            ("Gestión", ["Atención de solicitudes de seguridad", "Gestión de vulnerabilidades", "Reportes de postura de seguridad"]),
        ],
        "verticals": ["empresas", "gobierno", "telcos"],
    },
    {
        "slug": "negocios-web", "name": "Desarrollo de Negocios Web",
        "short": "Sitios, aplicaciones y experiencias digitales que generan negocio.",
        "what": "Creamos experiencias digitales para marcas y soluciones empresariales que optimizan la productividad: desde la asesoría inicial hasta el desarrollo de sitios y aplicaciones conectadas a tu operación.",
        "groups": [
            ("Servicios", ["Asesoría para negocios web", "Desarrollo web y de aplicaciones", "Aplicaciones nativas de negocio", "Experiencias inmersivas para marcas"]),
        ],
        "verticals": ["empresas", "gobierno"],
    },
    {
        "slug": "agentes-ia", "name": "Agentes de Inteligencia Artificial",
        "short": "Agentes omnicanal que comprenden, ejecutan y resuelven tareas de principio a fin.",
        "what": "Agentes de inteligencia artificial que atienden a tus clientes y resuelven flujos administrativos dentro de un solo sistema, en cualquier canal e idioma, integrados con las herramientas que ya utilizas.",
        "groups": [
            ("Capacidades", ["Agentes omnicanal (chat, voz y correo)", "Plataforma sin código", "Mejora continua en tiempo real", "Humanos digitales"]),
            ("Integración", ["Canales de mensajería", "CRM y sistemas centrales", "Analítica de conversaciones", "Multilingüe"]),
        ],
        "verticals": ["empresas", "gobierno", "telcos"],
    },
]

ALL = GRID + EXTRA


def service_options(selected=None):
    opts = ['<option value="">Selecciona una opción</option>']
    for s in ALL:
        sel = " selected" if s["slug"] == selected else ""
        opts.append(f'<option value="{s["slug"]}"{sel}>{s["name"]}</option>')
    opts.append('<option value="otro">Otro / aún no lo sé</option>')
    return "".join(opts)
