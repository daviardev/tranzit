"""
ENRICH-KEYWORDS.PY
==================
Adds colloquial Colombian keywords to all LawEntry markdown files.

Run: python3 scripts/enrich-keywords.py

This script injects hundreds of Colombian colloquial expressions,
slang, and everyday phrasings so that queries like "el tombo me
pidió lucas pa no multarme" match the right legal articles.

HOW TO MODIFY:
- Add new patterns to the PATTERNS dict below.
- Each key is a substring that matches article IDs (e.g. "soat").
- Each value is a list of keywords/synonyms to add.
"""

import os
import re

SRC = os.path.join(os.path.dirname(__file__), "..", "src", "content")

GENERIC_ADDITIONS = [
    "código nacional de tránsito",
    "ley 769 de 2002",
]

PATTERNS: dict[str, list[str]] = {

    # ========================================================
    # ABUSOS
    # ========================================================

    "maltrato-verbal": [
        "me insultó", "me gritó", "agresivo", "amenaza", "me amenazó",
        "me humilló", "agente abusivo", "abuso de autoridad",
        "me trató mal", "fue grosero", "me faltó al respeto",
        "gritos", "humillación", "trato degradante", "grosería",
        "insulto", "abuso policial", "falta disciplinaria",
        "cómo denunciar maltrato de agente de tránsito",
        "agente me insultó", "me trató como delincuente",
        "tombo grosero", "el tombo me gritó", "me dijo groserías",
        "tránsito abusivo", "agente malgeniado", "me maltrató el agente",
        "me humilló el tránsito", "abuso del agente de tránsito",
        "maltrato de la policía de tránsito", "cómo poner una queja",
        "derecho de petición por maltrato", "me discriminó el agente",
        "me trató mal por mi color de piel", "discriminación en retén",
        "me trataron como un delincuente", "maltrato psicológico",
        "abuso verbal", "violencia verbal", "agresión verbal",
        "me gritó el tombo", "tránsito me faltó al respeto",
    ],

    "detencion-arbitraria": [
        "reten", "detención", "demora", "tiempo excesivo",
        "me retuvieron", "me tuvo esperando", "retención ilegal",
        "abuso policial", "me tienen detenido sin razón",
        "cuánto tiempo me pueden tener en un retén",
        "detención arbitraria", "privación ilegal de la libertad",
        "no me dejan ir", "me tienen retenido", "me llevaron detenido",
        "me tienen en la URI", "estoy detenido en tránsito",
        "me tienen en el CAI", "detención injusta", "retención ilegal",
        "cuánto dura un retén", "demora excesiva en retén",
        "reten arbitario", "privación de la libertad sin orden",
        "captura ilegal", "detención sin motivo", "abuso en retén",
        "me llevaron a la URI sin razón", "cuánto tiempo en retén",
        "reten de tránsito injusto", "detención arbitraria agente",
        "retención sin justa causa", "reten de transito injusto",
        "me tuvieron horas en el retén", "horas en el retén",
        "reten excesivo", "inmovilización injusta", "me tienen preso",
    ],

    "exigir-dinero": [
        "coima", "soborno", "dinero", "plata", "mordida",
        "corrupción", "agente corrupto", "sobornó",
        "me pidió plata", "me pidió dinero", "me pidió soborno",
        "le pagué al agente", "arreglo con el agente",
        "soborno a agente de tránsito", "qué hago si me pide plata",
        "denunciar soborno", "extorsión", "me pidió $",
        "me pidió billete", "me pidió lucas", "me pidió para no multarme",
        "me pidio una platica", "le di plata al tombo",
        "le pagué al tránsito", "cuánto le doy al tombo",
        "lleve al agente", "arreglo", "arreglo con tránsito",
        "me pidio 50", "me pidio 100", "me pidio 200",
        "cuánto vale que no me multe", "me pidió que le colabore",
        "échele algo al agente", "corrupción de tránsito",
        "denunciar policía corrupto", "tombo corrupto",
        "me pidió plata para no llevarse el carro",
        "me pidió plata para no inmovilizar", "soborno en retén",
        "me pidió la cédula con plata", "extorsión en retén",
        "me pidió 20 lucas", "me pidió 50 lucas",
        "me pidió una colaboración", "colaboración pa el café",
        "pal refresco", "pa la gaseosa", "pa la cerveza",
        "me pidio pa no hacerme el comparendo",
        "me pidio pa no inmovilizarme", "me pidio pa no llevarme a patios",
        "me quitó la licencia y me pidio plata",
        "cuánto vale sobornar tránsito", "cómo denunciar coima",
        "donde denunciar coima", "doide", "doide procuraduría",
        "procuraduría", "denunciar tombo",
    ],

    "codigo-policia-abuso": [
        "abuso de autoridad", "policía abusivo", "agente abusivo",
        "código de policía", "conflicto con policía",
        "denunciar abuso policial", "qué hago si un policía me agrede",
        "policía me pegó", "policía me golpeó", "golpiza policial",
        "uso excesivo de la fuerza", "fuerza desproporcionada",
        "policía me esposó sin razón", "maltrato policial",
        "policía me empujó", "policía me tiró al piso",
        "abuso de la fuerza", "policía me maltrató físicamente",
        "golpes de policía", "policía me agredió",
        "lesiones por policía", "cómo demandar a un policía",
        "abuso de autoridad del tránsito", "policía de tránsito abusivo",
        "me golpeó el tránsito", "me agredió el agente",
        "uso excesivo de la fuerza por tránsito",
        "abuso de fuerza por policía de tránsito",
        "denunciar policía de tránsito", "código nacional de policía",
        "cómo poner denuncia contra un policía",
        "qué hago si un policía me abusa",
        "dónde denunciar a un policía",
    ],

    # ========================================================
    # ALCOHOLEMIA
    # ========================================================

    "examen-de-embriaguez": [
        "soplar", "alcoholímetro", "prueba de alcoholemia",
        "baboso", "probador", "borracho", "tomado",
        "me hicieron soplar", "me pidieron soplar", "prueba de alcohol",
        "dos cervezas", "una cerveza", "cómo es la prueba de alcoholemia",
        "me pueden hacer soplar", "negarme a soplar",
        "qué pasa si no soplo", "me pararon borracho",
        "me hicieron soplar en el retén", "me pidieron soplar y soplé",
        "soplé y di positivo", "cuánto tiempo tengo que soplar",
        "cómo funciona el alcoholímetro", "prueba de alcoholemia en vía",
        "examen de embriaguez obligatorio", "qué pasa si soplo positivo",
        "me mandaron a hacer examen de embriaguez",
        "puedo negarme a la prueba de alcoholemia",
        "dónde me hacen el examen", "examen de sangre por alcohol",
        "toma de muestra de sangre", "alcoholemia en vía pública",
        "control de alcoholemia", "puesto de control alcoholemia",
        "reten de alcoholemia", "me pararon por alcoholemia",
        "sopladorcito", "soplar el aparatico", "el bombillo ese",
        "soplar el pitillo", "prueba de alcoholemia obligatoria",
        "sopló y le dio", "cuánto marca el alcoholímetro",
        "me pidieron hacer la prueba de embriaguez",
        "examen de embriaguez en tránsito",
        "me pararon por sospecha de alcohol",
    ],

    "grados-de-alcoholemia": [
        "nivel de alcohol", "grado de alcoholemia", "alcohol en sangre",
        "cuánto alcohol puedo tomar", "límite de alcohol conductor",
        "cero alcohol", "alcohol 0.0", "sancion por alcohol",
        "licor", "cerveza", "whisky", "ron", "vino",
        "tomé y manejé", "manejar después de tomar",
        "cuántas cervezas puedo tomar para manejar",
        "una cerveza manejando", "dos cervezas manejando",
        "límite de alcohol motociclista", "límite de alcohol conductor",
        "grado 1 de embriaguez", "grado 2 de embriaguez",
        "grado 3 de embriaguez", "primer grado de embriaguez",
        "nivel 1 de alcohol", "alcohol grado 1", "alcohol grado 2",
        "alcoholemia grado 1", "alcoholemia grado 2",
        "cuánto es el límite de alcohol",
        "cero alcohol en conductores", "tolerancia cero alcohol",
        "ley cero alcohol", "pérdida de licencia por alcohol",
        "multa por alcohol en conductores",
        "sanción por embriaguez", "comparendo por alcohol",
        "cuánto es la multa por manejar tomado",
        "manejar tomado consecuencias", "manejar borracho sanción",
        "polo", "pola", "una pola manejando",
        "unos tragos", "unas cervezas", "salí a tomar y manejé",
        "tomé dos polas", "tomé tres cervezas",
        "manejar después de unos tragos",
    ],

    "negativa-a-prueba": [
        "negarme a soplar", "no soplar", "rechazar prueba",
        "negativa a la prueba", "no quiero soplar",
        "me negué a la prueba de alcoholemia",
        "qué pasa si me niego a soplar",
        "retención de licencia por no soplar",
        "no sople", "me negué a soplar que pasa",
        "me negué al alcoholímetro", "rechacé la prueba de alcohol",
        "consecuencias de negarse a soplar",
        "negativa a la prueba de embriaguez",
        "qué pasa si no quiero hacer la prueba",
        "me puedo negar a la prueba de alcohol",
        "negarme al examen de embriaguez",
        "me rehusé a soplar", "no quise soplar",
        "suspensión de licencia por no soplar",
        "perder licencia por no soplar",
        "cuánto me suspenden la licencia si no soplo",
        "me da miedo soplar", "tengo miedo de soplar",
        "no sople y me quitaron la licencia",
        "es obligatorio soplar", "puedo negarme soplar",
        "pérdida de licencia por negarse a soplar",
        "multa por negarse a alcoholemia",
    ],

    "suspension.*alcohol": [
        "suspensión de licencia", "perder la licencia",
        "me quitaron la licencia", "choque ebrio",
        "accidente por alcohol", "cárcel por choque ebrio",
        "suspendieron la licencia", "licencia suspendida",
        "perder el pase", "me quitaron el pase",
        "suspensión del pase por alcohol",
        "cuánto me suspenden la licencia",
        "tiempo de suspensión de licencia",
        "recuperar licencia suspendida", "cómo recuperar la licencia",
        "licencia suspendida por alcohol", "suspensión 10 años",
        "suspensión 5 años", "años sin licencia",
        "no puedo manejar por años", "cárcel por manejar borracho",
        "homicidio culposo por alcohol", "muerte por accidente alcohol",
        "choque por borracho", "choqué borracho",
        "choque causado por alcohol", "accidente ebrio consecuencias",
        "me quitaron la licencia por alcohol",
        "suspensión de licencia por embriaguez",
        "recuperar pase después de suspensión",
        "cómo vuelvo a sacar la licencia",
        "cuánto vale recuperar licencia suspendida",
    ],

    # ========================================================
    # DERECHOS
    # ========================================================

    "trato-digno": [
        "trato digno", "derechos en retén", "qué hacer en un retén",
        "me pueden pedir documentos", "derechos del conductor",
        "cómo comportarse en un retén", "reten de tránsito derechos",
        "qué hace un agente de tránsito",
        "derechos del ciudadano en retén",
        "derechos constitucionales en tránsito",
        "qué puede hacer el tránsito", "hasta dónde puede un agente",
        "derecho a no ser retenido", "derecho a la libertad",
        "me pueden detener por una multa",
        "derechos humanos en retén", "derechos del detenido",
        "derechos del infractor", "derechos del conductor detenido",
        "qué derechos tengo en un retén",
        "derecho a llamar un abogado en retén",
        "derecho a hacer una llamada", "derecho a un abogado",
        "me pueden esposar por infracción",
        "derecho a que me lean mis derechos",
        "me leyeron los derechos", "cárcel por infracción",
        "ir a la cárcel por multa", "derecho a defensa",
    ],

    "debido-proceso": [
        "60 minutos", "plazo para arreglar",
        "arreglar en el sitio", "reparar en el lugar",
        "tiempo para arreglar", "subsanar",
        "solicitar 60 minutos", "me dieron 60 minutos",
        "detención", "retención", "no me dejan ir",
        "apelar", "rechazar", "pelear la multa",
        "no estoy de acuerdo", "quiero pelear", "defenderme",
        "descargos", "audiencia pública", "recurso de reposición",
        "me quiero defender",
        "debido proceso administrativo",
        "derecho a la defensa", "derecho de contradicción",
        "principio de legalidad", "derecho al debido proceso",
        "puedo apelar un comparendo", "cómo apelar",
        "términos para apelar", "plazo para presentar descargos",
        "cuánto tiempo tengo para apelar", "apelar multa de tránsito",
        "inconformidad con comparendo", "quiero pelear el comparendo",
        "me multaron injustamente", "multa injusta",
        "comparendo injusto", "cómo reclamar un comparendo",
        "cómo impugnar un comparendo", "descargos comparendo",
        "audiencia para comparendo", "recurso de apelación",
        "defensa en comparendo",
    ],

    "grabar-agentes": [
        "filmar", "grabación", "video", "celular", "grabar",
        "me quitó el celular", "borró el video",
        "me confiscaron el celular", "no me dejó grabar",
        "derecho a grabar", "es legal grabar",
        "grabar a policía", "grabar agente de tránsito",
        "grabar con el celular", "grabar en retén",
        "puedo grabar a los policías",
        "es legal grabar a un agente de tránsito",
        "el agente me pidió que no grabara",
        "me pidió que borrara el video",
        "derecho a filmar a la policía",
        "puedo grabar el comparendo",
        "grabar como evidencia", "evidencia en video",
        "prueba de video", "video de abuso policial",
        "cómo grabar sin que se den cuenta",
        "grabar ocultamente", "grabar a escondidas",
        "el tránsito me quitó el celular",
        "me decomisaron el teléfono por grabar",
    ],

    # ========================================================
    # DISPOSICIONES FINALES
    # ========================================================

    "ejecucion-de-sanciones": [
        "prescripción", "se venció la multa", "ya pasó mucho tiempo",
        "caducó la multa", "ya no tengo que pagar",
        "cobro de multas", "ejecución de sanciones",
        "multa prescribió", "ya no debo la multa",
        "prescripción de comparendo", "prescripción de multas",
        "cuándo prescribe una multa",
        "tiempo para prescripción de multas",
        "cuánto tiempo prescribe una multa de tránsito",
        "prescripción de infracciones de tránsito",
        "ya se venció el plazo de la multa",
        "multa antigua ya no vale",
        "prescripción de sanciones", "cobro coactivo",
        "embargo por multa", "me embargaron por multa de tránsito",
        "multa en cobro jurídico", "proceso de cobro",
        "notificación de multa", "no me notificaron la multa",
    ],

    "destinacion-de-multas": [
        "a dónde va el dinero de las multas", "destino de multas",
        "para qué sirven las multas", "fondos de multas",
        "dinero de comparendos", "para dónde va la plata de las multas",
        "en qué se gastan las multas",
        "presupuesto de multas de tránsito",
        "los comparendos para dónde van",
        "destinación de los recursos de multas",
        "excedentes de multas", "fondo de seguridad vial",
    ],

    "aplicacion-de-otros": [
        "qué código aplica", "norma aplicable",
        "leyes de tránsito aplicables", "códigos relacionados",
        "código penal en accidentes", "código disciplinario",
        "código de comercio transporte", "leyes complementarias",
        "normas supletorias", "normas aplicables al tránsito",
        "qué leyes rigen el tránsito en Colombia",
        "leyes de tránsito complementarias",
        "códigos que aplican al conductor",
    ],

    "disposiciones-finales": [
        "vigencia de la ley", "derogatorias", "presupuesto",
        "videovigilancia", "validez de la ley 769",
        "derogación de la ley 769",
        "qué artículos están vigentes",
        "artículos derogados", "ley 769 vigencia",
        "modificaciones a la ley 769",
        "cambios al código de tránsito",
        "actualización del código de tránsito",
        "nueva ley de tránsito", "reforma al código de tránsito",
        "versión actualizada del código de tránsito",
    ],

    # ========================================================
    # INFRACCIONES
    # ========================================================

    "infracciones-30-smldv": [
        "sin licencia", "sin soat", "sin revisión",
        "no tengo licencia", "no tengo soat",
        "soat vencido", "revisión vencida", "infracción grave",
        "multa de 30 salarios", "30 smldv",
        "conducción sin licencia", "manejar sin pase",
        "manejar sin licencia", "no tengo pase",
        "cogieron manejando sin licencia",
        "multa por no tener licencia", "cuánto vale no tener licencia",
        "cuánto es la multa por no tener soat",
        "multa soat vencido", "comparendo por soat vencido",
        "me pararon sin soat", "sin soat cuánto es la multa",
        "multa revisión técnico mecánica vencida",
        "revisión técnico mecánica vencida multa",
        "me pararon sin revisión",
        "manejar sin documentos del carro",
        "conducción sin documentos", "sin documentos multa",
        "no portar licencia", "no portar soat",
        "no portar revisión", "falta de documentos",
        "cuánto pagan por no tener soat",
        "comparendo por no tener documentos",
    ],

    "infracciones-15-smldv": [
        "multa", "comparendo", "infracción", "me multaron",
        "me pusieron comparendo", "cuánto vale la multa",
        "pagar multa", "smldv", "salario mínimo",
        "exceso de velocidad", "semáforo", "luz roja",
        "iba rápido", "me pasé el semáforo",
        "mal estacionado", "estacionar", "parquear",
        "sin casco", "casco", "celular",
        "hablando por celular", "manejando y celular",
        "cinturón", "sin cinturón", "pico y placa",
        "violé pico y placa", "pico y placa hoy",
        "manejar con celular", "multa por celular manejando",
        "manejar hablando por teléfono", "manejar con auriculares",
        "mal parqueado", "estacionado en lugar prohibido",
        "parqueado en zona prohibida", "me multaron por estacionar",
        "comparendo por mal estacionamiento",
        "comparendo por exceso de velocidad",
        "cuánto vale comparendo por semáforo",
        "me pasé el semáforo en rojo multa",
        "multa por pasar semáforo en rojo",
        "infracción por no usar cinturón",
        "multa por no usar cinturón de seguridad",
        "comparendo por Pico y Placa",
        "cuánto vale la multa del pico y placa",
        "cuánto vale un comparendo",
        "valor del comparendo 2025", "valor del comparendo 2026",
    ],

    "infracciones-45-smldv": [
        "embriaguez", "borracho", "alcohol",
        "exceso de velocidad grave", "carrera ilegal",
        "pique ilegal", "40 smldv", "45 smldv",
        "piques", "carreras clandestinas",
        "pique en la vía", "carreras en vía pública",
        "exceso de velocidad peligroso",
        "conducción temeraria", "manejar a alta velocidad",
        "alta velocidad sanción", "multa por piques",
        "comparendo por piques", "pique entre carros",
        "carrera de carros en vía pública",
        "velocidad excesiva grave",
    ],

    "infracciones-8-smldv": [
        "placas", "sin placas", "documentos",
        "licencia de tránsito", "tarjeta de propiedad",
        "fotos multas", "fotomultas",
        "sin placa", "sin placa delantera",
        "placa adulterada", "placa tapada",
        "placa ilegible", "no se ve la placa",
        "comparendo por placa", "multa por no tener placa",
        "multa por placa tapada",
        "fotomulta", "comparendo electrónico",
        "foto comparendo", "multa por cámara",
        "cámara de tránsito", "cámara de fotomultas",
        "me llegó una fotomulta", "cómo saber si tengo fotomultas",
        "fotomultas cómo pagar", "impugnar fotomulta",
        "cómo pelear una fotomulta", "fotocomparendo",
        "multa por cámaras de velocidad",
        "cámara detecta placa", "cámara de semáforo",
        "cámara de pico y placa", "radar de velocidad",
    ],

    "infracciones-4-smldv": [
        "bicicleta", "ciclista", "sin luces bicicleta",
        "casco bicicleta", "infracción bicicleta",
        "multa a ciclista", "comparendo para bicicleta",
        "me multaron en bici", "sanción a ciclista",
        "multa por no llevar luces en la bici",
        "comparendo por andar en bici sin casco",
        "bicicleta sin elementos de seguridad",
        "ciclista multado", "andaba en bici y me multaron",
        "infracciones para bicicletas",
    ],

    "infracciones-6-smldv": [
        "vehículo eléctrico", "bicicleta eléctrica",
        "patineta eléctrica", "monopatín",
        "vehículo de movilidad personal",
        "infracción vehículo eléctrico",
        "patineta", "patín eléctrico", "scooter",
        "monociclo eléctrico", "hoverboard",
        "multa por patineta eléctrica", "comparendo patineta",
        "dónde puedo andar en patineta",
        "regulación de patinetas eléctricas",
        "vehículos de movilidad personal normativa",
    ],

    # ========================================================
    # NORMAS DE COMPORTAMIENTO
    # ========================================================

    "documentos-requeridos": [
        "seguro", "sin soat", "no tengo soat", "soat vencido",
        "soat vigente", "pase", "carnet", "carné",
        "sin licencia", "no tengo pase", "no tengo licencia",
        "me quitaron la licencia", "moto", "qué papeles necesito",
        "documentos para manejar", "tarjeta de propiedad",
        "qué documentos piden", "licencia de conducción",
        "papeles del carro", "papeles de la moto",
        "documentos de la moto", "qué papeles tengo que llevar",
        "documentos obligatorios para conducir",
        "documentos para andar en moto",
        "documentos para andar en carro",
        "qué pide el tránsito", "qué documentos revisan",
        "licencia de tránsito", "tarjeta de propiedad vehículo",
        "certificado de seguro", "soat obligatorio",
        "revisión técnico mecánica", "documentos del vehículo",
        "no llevaba los papeles", "me pararon y no tenía papeles",
        "olvidé los documentos", "dejé los papeles en casa",
        "qué pasa si no tengo los documentos",
        "multa por no portar documentos",
        "comparendo por no tener documentos",
    ],

    "soat-seguro-obligatorio": [
        "seguro", "sin soat", "no tengo soat", "soat vencido",
        "soat vigente", "cómo sacar soat", "precio soat",
        "soat 2025", "soat 2026", "venció el soat",
        "se me venció el soat", "soat para moto",
        "grúa", "patios", "inmovilización por soat",
        "me llevaron el carro", "cómo sacar el carro de patios",
        "clasificación soat", "tipos de soat",
        "soat electrónico", "cómo consultar soat",
        "sofá", "me pararon y no tenía soat",
        "soat vencido me inmovilizaron", "cuánto vale el soat",
        "precio soat 2025 moto", "precio soat 2025 carro",
        "soat digital", "soat virtual", "comprar soat online",
        "dónde comprar soat", "cómo renovar soat",
        "soat por días", "soat temporal", "soat para moto de alto cilindraje",
        "venció el soat de mi moto", "se me venció el soat del carro",
        "me multaron por soat vencido", "comparendo por soat",
        "inmovilización por falta de soat",
        "cómo sacar el carro de patios sin soat",
        "vale la pena tener soat", "para qué sirve el soat",
        "cobertura del soat", "qué cubre el soat",
        "soat y accidente", "sofá de la moto",
        "el sofá", "pagar soat", "cómo pagar soat",
        "soat por internet", "soat Bancolombia",
    ],

    "soat-seguro-complementario": [
        "seguro complementario", "soat complementario",
        "seguro voluntario", "protección adicional",
        "accidente", "siniestro", "indemnización",
        "seguro todo riesgo", "seguro para daños a terceros",
        "seguro extra", "seguro más completo",
        "cuánto cubre el soat complementario",
        "soat complementario qué cubre",
        "cobertura adicional soat", "seguro para choque",
        "daños materiales", "daños a terceros",
        "seguro de daños", "protección vehicular",
        "mejor seguro para carro", "seguro recomendado",
    ],

    "normas-motocicletas": [
        "moto", "motocicleta", "en moto", "motero",
        "casco de moto", "sin casco", "casco sin placa",
        "casco con placa", "me pararon sin casco",
        "parrillero", "parrilla", "licencia para moto",
        "cilindraje", "pase para moto",
        "normas para motos", "reglas para motociclistas",
        "moto cómo conducir", "conducción de motocicleta",
        "casco certificado", "casco de seguridad",
        "chaleco reflectivo moto", "reflectivos",
        "parrillero hombre moto", "parrillero mujer moto",
        "cuántas personas en una moto",
        "moto con parrillero normas",
        "motos de alto cilindraje", "pico y placa para motos",
        "pico y placa moto", "moto pico y placa",
        "moto sin silenciador", "escape libre moto",
        "ruido de moto", "comparendo por ruido moto",
        "multa por escape libre", "moto con escape modificado",
        "modificación de moto", "moto modificada",
        "manillar alto", "manillar modificado",
        "moto con parlantes", "moto con música",
        "multa por parlantes en moto",
        "moto con luces navideñas", "moto con luces modificadas",
        "moto polarizada", "moto con polarizado",
        "espejos de moto", "espejos retrovisores moto",
        "moto sin espejos", "moto sin direccionales",
        "moto con direccionales rotas", "moto con plásticos rotos",
        "moto sin frenos", "frenos de moto",
    ],

    "normas-bicicletas": [
        "bicicleta", "ciclista", "en bici", "bici",
        "ciclovía", "ciclorruta", "carril bici",
        "casco de bici", "luces bici", "campana",
        "reflejantes", "prendas reflectivas",
        "normas de bicicleta", "reglas para ciclistas",
        "dónde andar en bici", "bicicleta en la calle",
        "bicicleta por la ciclorruta", "bicicleta en carretera",
        "elementos de seguridad bicicleta",
        "qué debe llevar una bicicleta",
        "luces delanteras y traseras bici",
        "casco para bicicleta obligatorio",
        "multa a ciclista", "comparendo para bicicleta",
        "bici en vía pública", "bicicleta en autopista",
        "bicicleta prohibida en vía", "dónde no puedo andar en bici",
        "bicicleta de noche", "luces para bicicleta nocturna",
        "chaleco reflectivo para bici",
        "campana para bicicleta", "freno de bicicleta",
    ],

    "limites-de-velocidad": [
        "exceso de velocidad", "iba rápido",
        "me multaron por velocidad", "radar",
        "fotomulta velocidad", "me tomaron la velocidad",
        "límite de velocidad", "a qué velocidad puedo ir",
        "velocidad máxima", "velocidad mínima",
        "cuál es el límite de velocidad",
        "límite de velocidad en ciudad",
        "límite de velocidad en carretera",
        "límite de velocidad en autopista",
        "límite de velocidad en zona escolar",
        "límite de velocidad en zona residencial",
        "me tomaron con radar", "radar de velocidad",
        "cámara de velocidad", "multa por radar",
        "iba a 100", "iba a 120",
        "excedí el límite de velocidad",
        "cuánto es la multa por exceso de velocidad",
        "comparendo por velocidad", "sanción por exceso velocidad",
        "velocidad permitida en Colombia",
        "velocidad máxima en Colombia",
    ],

    "luces": [
        "luz", "luz quemada", "luz fundida", "luz dañada",
        "luz rota", "farola", "faro", "bombillo", "foco",
        "sin luces", "luces delanteras", "luces traseras",
        "direccionales", "luces de freno", "alta y baja",
        "luces antiniebla", "luces exploradoras",
        "luz alta", "luz baja", "luz de carretera",
        "luz de cruce", "luz de posición",
        "luz de marcha", "luz diurna",
        "luz de freno no funciona", "direccionales dañadas",
        "faro quemado", "foco fundido",
        "me pararon por una luz dañada",
        "comparendo por falta de luces",
        "multa por luz dañada", "farola dañada",
        "luz trasera dañada", "luz delantera dañada",
        "multa por direccionales dañadas",
        "multa por frenos dañados", "freno delantero",
        "freno trasero", "luz de la placa",
        "luz de tablero", "luces interiores",
        "luces de emergencia", "luces estroboscópicas",
        "luces led", "luz neón", "luces personalizadas",
        "faros del carro", "farolas delanteras",
        "bombillo de la luz", "foco de la moto",
        "luz de la moto", "luz delantera de la moto",
        "luz trasera de la moto",
        "espejo retrovisor dañado", "espejos rotos",
        "se me dañó un espejo", "me pararon por el espejo",
        "espejos no originales", "espejos que no son de fábrica",
        "modificación de espejos",
    ],

    "estacionamiento": [
        "parquear", "estacionar", "parqueadero",
        "dónde puedo parquear", "estacionamiento prohibido",
        "no hay dónde parquear", "zona azul",
        "parquímetro", "parte de estacionamiento",
        "mal estacionado", "me multaron por estacionar",
        "estacionar en zona prohibida",
        "parquear en la calle", "parquear en andén",
        "parquear en ciclovía", "parquear frente a un garaje",
        "parquear en curva", "parquear en esquina",
        "parquear en doble fila", "parquear en sitio prohibido",
        "comparendo por mal parqueo",
        "multa por mal parqueadero",
        "grúa por mal parqueo", "se llevaron mi carro por mal parqueo",
        "inmovilización por mal estacionamiento",
        "patios por mal parqueo",
        "cuánto vale multa por mal parqueo",
        "estacionamiento para discapacitados",
        "zona de estacionamiento pago", "parquímetro cómo funciona",
        "no pagué parquímetro",
    ],

    "pico-y-placa": [
        "pico y placa", "hoy no puedo salir",
        "qué día no puedo", "me multaron por pico y placa",
        "pico y placa hoy", "pico y placa mañana",
        "excepción pico y placa", "pico y placa solidario",
        "violación pico y placa", "multa por pico y placa",
        "pico y placa para motos", "pico y placa moto",
        "pico y placa taxis", "pico y placa servicio público",
        "pico y placa en mi ciudad",
        "pico y placa Bogotá", "pico y placa Medellín",
        "pico y placa Cali", "pico y placa Barranquilla",
        "pico y placa Bucaramanga", "pico y placa Pereira",
        "pico y placa Armenia", "pico y placa Manizales",
        "pico y placa en Colombia",
        "me cogió el pico y placa",
        "cuánto vale la multa por pico y placa",
        "comparendo por pico y placa",
        "sanción por violar pico y placa",
        "cómo saber si tengo pico y placa",
        "consultar pico y placa",
        "excepción al pico y placa", "exención pico y placa",
        "pico y placa para vehículo eléctrico",
        "pico y placa para híbrido",
        "pico y placa para discapacitados",
        "pico y placa para médico",
        "pico y placa para carro compartido",
        "pico y placa solidario cómo funciona",
        "pico y placa solidario precio",
        "pico y cedula", "confundí pico y placa con pico y cédula",
    ],

    "conducta-general": [
        "comportamiento", "deberes del conductor",
        "cómo conducir", "normas de conducción",
        "buen conductor", "conducción responsable",
        "seguridad vial",
        "normas de comportamiento en la vía",
        "cómo ser buen conductor",
        "reglas de conducción defensiva",
        "conducción a la defensiva",
        "errores al conducir", "malos hábitos al manejar",
        "cortesía en la vía", "respeto entre conductores",
        "conducta en la vía pública",
        "normas para conductores Colombia",
    ],

    "intersecciones": [
        "cruce", "intersección", "giro", "derecha",
        "izquierda", "ceda el paso", "pare",
        "señal de pare", "me pasé el pare",
        "prelación", "quién tiene la vía",
        "quién pasa primero en una intersección",
        "preferencia en intersección",
        "cruce de vías", "cruce sin señalizar",
        "giro a la izquierda", "giro a la derecha",
        "cómo girar en una intersección",
        "glorieta", "rotonda",
        "cómo manejar en una glorieta",
        "quién tiene prioridad en una glorieta",
        "señal de ceda el paso",
        "señal de pare", "cruce peatonal",
        "bocacalle", "esquina",
    ],

    "carriles-adelantamiento": [
        "carril", "adelantar", "rebasamiento",
        "cambio de carril", "carril izquierdo",
        "carril derecho", "sobrepaso",
        "cómo adelantar correctamente",
        "cuándo puedo adelantar", "adelantamiento prohibido",
        "línea continua", "línea discontinua",
        "adelantar en curva", "adelantar en línea continua",
        "multa por adelantar en curva",
        "adelantar en zona prohibida",
        "cambio de carril brusco",
        "carril de aceleración", "carril de desaceleración",
        "carril exclusivo", "carril de bus",
        "carril de bicicleta", "carril de moto",
        "carril lento", "carril rápido",
        "cuál carril debo usar",
    ],

    "transito-semaforos": [
        "semáforo", "luz roja", "luz verde", "luz amarilla",
        "me pasé el semáforo", "me pasé el rojo",
        "señales de tránsito", "agente de tránsito",
        "control de tránsito", "reten",
        "semáforo en rojo", "semáforo en verde",
        "semáforo en amarillo", "me pasé el semáforo en amarillo",
        "multa por pasarse el semáforo",
        "comparendo por semáforo",
        "semáforo peatonal", "semáforo para peatones",
        "semáforo dañado", "semáforo en intermitente",
        "semáforo en mantenimiento",
        "pasarse el semáforo en rojo",
        "infracción por semáforo",
        "qué hacer si un semáforo está dañado",
        "señales del agente de tránsito",
        "señales manuales del agente",
        "agente de tránsito señales",
        "cómo interpretar señales del agente",
    ],

    "senales-de-transito": [
        "señal de tránsito", "señal", "pare", "ceda el paso",
        "zona escolar", "velocidad máxima",
        "señalización", "qué significa esa señal",
        "no entiendo las señales de tránsito",
        "señales preventivas", "señales reglamentarias",
        "señales informativas", "tipos de señales de tránsito",
        "señales verticales", "señales horizontales",
        "señal de pare", "señal de ceda el paso",
        "señal de velocidad máxima",
        "señal de velocidad mínima",
        "señal de prohibido estacionar",
        "señal de prohibido adelantar",
        "señal de zona escolar",
        "señal de curva peligrosa",
        "señal de descenso pronunciado",
        "señal de resalto", "señal de rompemuelle",
        "señal de paso peatonal",
        "señal de semáforo próximos",
        "señal de intersección",
        "señal de glorieta",
        "señal de dirección obligatoria",
        "señal de sentido único",
        "señal de doble vía",
        "señal de autopista",
    ],

    "velocidad": [
        "reducción de velocidad", "bajar la velocidad",
        "despacio", "lento", "zona escolar",
        "curva peligrosa", "reductor de velocidad",
        "policía acostado", "resalto", "rompemuelles",
        "reductor de velocidad", "reductor",
        "policía acostado en la vía",
        "resalto en la vía", "rompemuelle",
        "zona escolar velocidad", "velocidad en zona escolar",
        "velocidad controlada", "reduzca la velocidad",
        "bajar la velocidad en curva",
        "despacio zona escolar",
        "reductor de velocidad en vía",
        "qué significa policía acostado",
        "policía dormido",
    ],

    "equipo-de-carretera": [
        "equipo de carretera", "kit de carretera",
        "gato", "llanta de repuesto", "cruceta",
        "botiquín", "extintor", "señales de carretera",
        "qué debo llevar en el carro",
        "elementos de seguridad",
        "kit de carretera obligatorio",
        "elementos obligatorios en el carro",
        "qué debe tener un carro",
        "equipo de prevención", "señales reflectivas",
        "cono de seguridad", "triángulo de seguridad",
        "señales de peligro", "extintor para carro",
        "botiquín de primeros auxilios",
        "gato para cambiar llanta",
        "llanta de repuesto obligatoria",
        "cruceta para llantas",
        "caballete", "tacos",
        "cuerda de remolque",
        "qué herramientas llevar en el carro",
        "elementos de carretera Colombia",
        "qué pide tránsito en carretera",
        "me pararon y me pidieron el kit de carretera",
        "multa por no llevar kit de carretera",
    ],

    "transporte-publico": [
        "bus", "buseta", "microbús", "taxi",
        "transporte público", "pasajero", "ruta",
        "cómo quejarse del transporte público",
        "derechos del pasajero",
        "transporte público en Colombia",
        "bus urbano", "bus intermunicipal",
        "buseta de servicio público",
        "taxi en Colombia", "servicio público de transporte",
        "derechos del usuario de transporte público",
        "cómo poner una queja de un bus",
        "queja contra conductor de bus",
        "accidente de bus", "choque de bus",
        "bus sobrecupo", "bus lleno",
        "bus con exceso de pasajeros",
        "parada de bus", "ruta de bus",
        "cómo saber qué bus tomar",
    ],

    "transporte-escolar": [
        "bus escolar", "transporte escolar",
        "ruta escolar", "niños en bus",
        "requisitos bus escolar", "señal bus escolar",
        "bus de colegio", "transporte de estudiantes",
        "normas para transporte escolar",
        "seguridad en transporte escolar",
        "bus escolar normas", "ruta escolar requisitos",
        "padre de familia bus escolar",
        "comparendo bus escolar", "infracción bus escolar",
        "señal de bus escolar", "pare bus escolar",
    ],

    "materiales-peligrosos": [
        "carga peligrosa", "material peligroso",
        "transporte de gasolina", "explosivos",
        "químicos peligrosos", "transporte de combustible",
        "transporte de mercancías peligrosas",
        "normas para transporte de peligrosos",
        "vehículo con materiales peligrosos",
        "señal de materiales peligrosos",
        "transporte de gas", "transporte de químicos",
        "transporte de inflamables",
        "requisitos para transportar peligrosos",
        "multa por transporte de peligrosos",
    ],

    "vehiculos-carga": [
        "carga", "camión", "camioneta",
        "peso bruto vehicular", "sobrecarga",
        "exceso de carga", "capacidad de carga",
        "transporte de carga", "mercancía",
        "camión de carga", "camioneta de carga",
        "vehículo de carga pesada",
        "multa por sobrecarga",
        "comparendo por exceso de carga",
        "peso máximo permitido",
        "medidas de vehículo de carga",
        "dimensiones de carga",
        "estiba de carga", "amarre de carga",
        "carga mal amarrada", "carga suelta",
        "multa por carga mal amarrada",
        "se me cayó la carga",
    ],

    "revision-tecnico-mecanica": [
        "tecnomecánica", "revisión técnico mecánica",
        "RTM", "venció la tecnomecánica", "no tengo revisión",
        "CDA", "revisión del carro", "cada cuánto es la revisión",
        "me pararon y la tecnomecánica estaba vencida",
        "revisión técnico mecánica vencida",
        "revisión del carro vencida",
        "dónde hacer la revisión técnico mecánica",
        "CDA centro de diagnóstico automotor",
        "cada cuánto se hace la revisión",
        "cada año revisión", "cada dos años revisión",
        "revisión para moto", "revisión para carro",
        "cuánto cuesta la revisión",
        "precio revisión técnico mecánica",
        "revisión técnico mecánica moto",
        "me pararon sin revisión",
        "multa por no tener revisión",
        "comparendo por revisión vencida",
        "inmovilización por revisión vencida",
        "patios por revisión vencida",
        "cómo sacar la revisión", "cómo agendar revisión",
        "revisión técnico mecánica obligatoria",
        "venció la RTM", "RTM vencida",
        "revisión del carro cada cuánto",
    ],

    "planes-de-movilidad": [
        "movilidad", "plan de movilidad",
        "restricción vehicular", "contaminación",
        "día sin carro", "día sin moto",
        "plan de movilidad urbana",
        "movilidad sostenible", "movilidad en Bogotá",
        "restricción ambiental", "pico y placa ambiental",
        "restricción por contaminación",
        "medidas de movilidad",
        "plan de descongestión",
    ],

    "clasificacion-de-vias": [
        "tipo de vía", "qué vía es", "autopista",
        "carretera", "vía urbana", "vía rural",
        "arteria", "vía principal", "vía secundaria",
        "clasificación de vías en Colombia",
        "vía nacional", "vía departamental",
        "vía municipal", "vía terciaria",
        "autopista nacional", "carretera nacional",
        "vía de montaña", "vía de terreno plano",
        "vía en buen estado", "vía en mal estado",
        "responsabilidad del estado por vías",
    ],

    "educacion-vial": [
        "curso de tránsito", "educación vial",
        "aprender a manejar", "examen de tránsito",
        "licencia por primera vez",
        "curso de conducción", "escuela de conducción",
        "examen práctico de conducción",
        "examen teórico de conducción",
        "cómo sacar la licencia por primera vez",
        "requisitos para licencia de conducción",
        "clases de manejo", "profesor de manejo",
        "autoescuela", "academia de conducción",
        "simulacro de examen de tránsito",
        "preguntas del examen de tránsito",
        "examen de tránsito Colombia",
        "pista de aprendizaje", "pista de conducción",
    ],

    "parrillero-motocicleta": [
        "parrillero", "acompañante moto",
        "en moto con alguien", "parrilla moto",
        "cuántos en una moto", "moto dos personas",
        "parrillero moto", "parrillera moto",
        "moto con acompañante",
        "casco para parrillero", "casco para acompañante",
        "parrillero sin casco",
        "multa por parrillero sin casco",
        "cuántas personas caben en una moto",
        "moto con tres personas",
        "prohibido parrillero hombre",
        "parrillero mujer permitido",
        "parrillero en moto de alto cilindraje",
    ],

    "seguridad-pasajeros": [
        "cinturón de seguridad", "seguridad",
        "cinturón", "no uso cinturón",
        "multa por no usar cinturón", "silla para niños",
        "niños en el carro", "seguridad infantil",
        "cinturón de seguridad obligatorio",
        "todos con cinturón",
        "silla de seguridad para niños",
        "asiento para bebé en el carro",
        "niños en el asiento trasero",
        "niños en silla de seguridad",
        "multa por niños sin silla",
        "comparendo por no llevar niños en silla",
        "seguridad vial para niños",
        "cinturón de seguridad trasero",
    ],

    "reduccion-velocidad": [
        "bajar la velocidad", "despacio", "lento",
        "curva", "zona escolar", "velocidad controlada",
        "reduzca la velocidad",
        "velocidad reducida",
        "conduzca despacio",
        "disminuir la velocidad",
        "reductor de velocidad",
        "zona de velocidad controlada",
        "velocidad máxima 30", "velocidad máxima 40",
        "zona 30", "zona 40",
    ],

    "proteccion-ambiental": [
        "contaminación", "emisiones", "humo",
        "carro ecológico", "gases contaminantes",
        "ruido", "escape ruidoso",
        "multa por contaminación",
        "vehículo contaminante",
        "humo negro del carro", "humo negro moto",
        "comparendo por contaminación",
        "comparendo ambiental",
        "multa por ruido excesivo",
        "escape libre multa",
        "vehículo con escape modificado",
        "multa por humo contaminante",
        "revisión de emisiones",
        "emisiones contaminantes vehículo",
        "carro ecológico beneficios",
        "vehículo eléctrico ventajas",
        "descuento en impuestos por carro eléctrico",
    ],

    # ========================================================
    # PROCEDIMIENTOS
    # ========================================================

    "subsanar-infracciones": [
        "60 minutos", "plazo para arreglar",
        "arreglar en el sitio", "reparar en el lugar",
        "tiempo para arreglar", "subsanar",
        "cuánto tiempo tengo para arreglar",
        "me pueden dar 60 minutos", "solicitar 60 minutos",
        "me dieron 60 minutos",
        "subsanar infracción", "subsanación de comparendo",
        "qué infracciones son subsanables",
        "infracciones subsanables Colombia",
        "cómo subsanar una infracción",
        "60 minutos para arreglar la falla",
        "plazo de 60 minutos",
        "subsanar en el sitio",
        "infracción subsanable",
        "no todas las infracciones se pueden subsanar",
    ],

    "procedimiento-para-comparendo": [
        "cómo es un comparendo", "procedimiento",
        "firma del comparendo", "recibir comparendo",
        "me pusieron un comparendo", "qué sigue después del comparendo",
        "cómo se hace un comparendo",
        "pasos del comparendo",
        "qué pasa después del comparendo",
        "procedimiento después de la multa",
        "me llegó el comparendo a casa",
        "notificación del comparendo",
        "comparendo notificación",
        "cómo notifican un comparendo",
        "comparendo en sitio", "comparendo por correo",
        "comparendo por fotomulta",
    ],

    "procedimiento-accidentes": [
        "accidente", "choque", "colisión", "chocar",
        "me chocaron", "choqué", "parte de accidente",
        "cómo hacer después de un accidente",
        "accidente de tránsito qué hacer",
        "lesionados", "heridos", "fallecidos",
        "seguro por accidente",
        "choqué qué hago",
        "me chocaron qué hago",
        "pasos después de un accidente",
        "qué hacer en un accidente de tránsito",
        "primeros pasos en un accidente",
        "aseguradora accidente",
        "parte de accidente amigable",
        "declaración de accidente",
        "atestado", "croquis del accidente",
        "fotos del accidente", "evidencia accidente",
        "testigos accidente",
        "accidente con lesionados",
        "accidente con muertos",
        "accidente leve", "accidente grave",
        "choque simple", "choque múltiple",
    ],

    "simit": [
        "simit", "consultar multas", "pagar multas",
        "cómo pagar una multa", "dónde pagar multa",
        "multas pendientes", "deuda de tránsito",
        "consultar comparendos", "pago de comparendos",
        "simit consultar", "simit pagar",
        "consultar multas por placa",
        "consultar comparendos por placa",
        "cómo saber si tengo multas",
        "cuánto debo en multas",
        "pagar comparendos online",
        "pagar multas de tránsito por internet",
        "simit en línea",
        "simit página oficial",
        "simit consulta de comparendos",
        "simit pago virtual",
        "deuda de comparendos",
        "multas de tránsito consulta",
    ],

    "impugnar-comparendo": [
        "impugnar", "disputar multa", "no estoy de acuerdo",
        "cómo pelear una multa", "reclamar comparendo",
        "injusto", "me multaron injustamente",
        "cómo defenderme de una multa",
        "descargos comparendo",
        "apelar comparendo", "apelar multa",
        "recurso contra comparendo",
        "recurso de reposición comparendo",
        "cómo impugnar un comparendo",
        "quiero pelear el comparendo",
        "me parece injusto el comparendo",
        "dónde presentar descargos",
        "descargos por comparendo",
        "formato de descargos comparendo",
        "cómo redactar descargos",
        "ejemplo de descargos comparendo",
        "descargos por fotomulta",
        "impugnar fotomulta",
        "cómo impugnar una fotomulta",
        "comparendo injusto qué hacer",
        "no cometí la infracción",
        "me multaron por error",
        "error del agente", "error del radar",
        "cámaras mal calibradas",
        "radar mal calibrado",
        "defensa comparendo",
    ],

    "audiencia-publica": [
        "audiencia", "citación", "comparecencia",
        "me citaron a audiencia", "qué pasa en la audiencia",
        "cómo prepararse para una audiencia",
        "audiencia por comparendo",
        "citación a audiencia tránsito",
        "audiencia pública de tránsito",
        "qué hacer en una audiencia",
        "asistir a audiencia",
        "no asistí a la audiencia",
        "consecuencias de no ir a la audiencia",
        "audiencia de descargos",
        "audiencia de impugnación",
        "audiencia de multa",
    ],

    "runt": [
        "runt", "registro único nacional de tránsito",
        "consultar runt", "cómo registrarse en runt",
        "historial de multas", "pase a punto",
        "runt consultar", "runt registro",
        "registro en runt", "cómo saber si estoy en el runt",
        "runt placa", "consultar runt por placa",
        "runt vehículo", "runt conductor",
        "historial del conductor",
        "puntos en la licencia",
        "sistema de puntos conductor",
    ],

    "prescripcion-multas": [
        "prescripción", "se venció la multa",
        "ya pasó mucho tiempo", "caducó la multa",
        "ya no tengo que pagar", "cuánto tiempo para prescribir",
        "prescripción de comparendos",
        "prescripción de multas de tránsito",
        "cuándo prescribe una multa",
        "plazo de prescripción de multas",
        "multas prescriben",
        "prescripción de sanciones de tránsito",
        "término de prescripción",
        "tres años prescribe multa",
    ],

    "informe-policial-accidente": [
        "informe de accidente", "croquis",
        "parte policial", "denuncia de accidente",
        "informe de tránsito", "informe de la policía",
        "informe del accidente",
        "cómo obtener el informe policial",
        "copias del informe",
        "informe de accidente de tránsito",
        "IPAT", "informe policial de accidente de tránsito",
    ],

    "concepto-tecnico-accidente": [
        "concepto técnico", "peritaje", "investigación accidente",
        "causa del accidente", "análisis de siniestro",
        "dictamen técnico", "concepto de accidente",
        "peritaje de accidente",
        "investigador de accidentes",
        "análisis de choque",
        "dictamen de la aseguradora",
    ],

    "facilidades-pago": [
        "facilidades de pago", "pagar a cuotas",
        "descuento multa", "pronto pago",
        "50% de descuento", "pagar 50%",
        "descuento por pronto pago",
        "pagar la multa con descuento",
        "cuánto descuento tengo",
        "plazo para pagar con descuento",
        "descuento del 50% comparendo",
        "pago oportuno descuento",
        "cómo pagar con descuento",
        "días para pagar con descuento",
        "pagar comparendo con descuento",
    ],

    "paz-y-salvo": [
        "paz y salvo", "certificado de paz y salvo",
        "no debo multas", "todo en orden",
        "vender carro paz y salvo",
        "cómo sacar paz y salvo",
        "paz y salvo de multas",
        "paz y salvo para vender vehículo",
        "certificado de paz y salvo tránsito",
        "requisito paz y salvo",
        "debo multas", "cómo saber si debo multas",
    ],

    "infracciones-penales": [
        "accidente con heridos", "lesiones",
        "muerte en accidente", "homicidio culposo",
        "cárcel por accidente", "detención por accidente",
        "lesiones personales en accidente",
        "homicidio en accidente de tránsito",
        "cárcel por choque",
        "accidente con fallecidos",
        "proceso penal por accidente",
        "indemnización por accidente",
        "responsabilidad penal accidente",
        "abogado para accidente",
        "conciliación por accidente",
    ],

    # ========================================================
    # LEYES COMPLEMENTARIAS
    # ========================================================

    "codigo-general-disciplinario": [
        "falta disciplinaria", "quéjese del agente",
        "denunciar agente", "abuso de autoridad",
        "código disciplinario",
        "procuraduría", "denunciar en procuraduría",
        "quéjese en la procuraduría",
        "falta disciplinaria de agente",
        "agente de tránsito falta",
        "sanción disciplinaria agente",
        "cómo denunciar a un agente",
        "denunciar a un tombo",
        "código disciplinario único",
        "faltas gravísimas agente",
        "investigación disciplinaria",
    ],

    "60-minutos-gracia": [
        "60 minutos", "estacionamiento",
        "no pague parquímetro", "gracia estacionamiento",
        "60 minutos de gracia",
        "zona azul 60 minutos",
        "primera hora gratis",
        "parquímetro 60 minutos",
        "60 minutos sin pagar",
        "estacionar 60 minutos gratis",
        "no pagué parquímetro los primeros 60",
    ],

    "ansv": [
        "seguridad vial", "agencia de seguridad vial",
        "estadísticas de tránsito", "planes de seguridad vial",
        "ansv Colombia", "agencia nacional de seguridad vial",
        "observatorio de seguridad vial",
        "campañas de seguridad vial",
        "prevención de accidentes",
        "educación vial ansv",
    ],

    "probici": [
        "bicicleta", "bici", "ciclista",
        "beneficios para bicicletas",
        "ley probici", "1811 de 2016",
        "ley de bicicleta",
        "incentivos para ciclistas",
        "beneficios para usar bicicleta",
        "probici ley",
        "días sin carro y sin moto",
        "ciclovía dominical",
        "exención pico y placa bicicleta",
    ],

    "comparendo-ambiental": [
        "ambiental", "comparendo ambiental",
        "basura", "desechos", "contaminación",
        "multa por contaminar", "ecológico",
        "comparendo por basura",
        "comparendo por sacar basura",
        "comparendo por quemar basura",
        "comparendo por arrojar desechos",
        "multa por arrojar basura a la calle",
        "cultura ciudadana",
    ],

    # ========================================================
    # DEFINICIONES
    # ========================================================

    "accidente-de-transito": [
        "accidente", "choque", "colisión", "siniestro",
        "accidente de tránsito", "chocar", "me chocaron",
        "parte de accidente",
        "qué es un accidente de tránsito",
        "tipos de accidentes",
        "accidente vehicular",
        "choque de frente", "choque lateral",
        "choque por alcance", "choque en intersección",
        "vuelco", "volcamiento",
        "atropellamiento", "atropellar",
        "caída de vehículo",
        "accidente de moto", "accidente de carro",
        "accidente con bus",
    ],

    "alcoholemia": [
        "alcohol", "alcoholemia", "borracho", "tomado",
        "alcoholímetro", "soplar",
        "qué es la alcoholemia",
        "prueba de alcoholemia",
        "examen de alcoholemia",
        "control de alcoholemia",
        "alcoholemia en Colombia",
        "alcoholemia positiva",
        "alcoholemia negativa",
    ],

    "alcoholuria": [
        "alcoholuria", "alcohol en orina",
        "examen de alcohol", "prueba de alcohol",
        "examen de orina para alcohol",
        "prueba de alcohol en orina",
    ],

    "alcoholometria": [
        "alcoholometría", "nivel de alcohol",
        "prueba de alcoholemia", "medición de alcohol",
        "medición de alcohol en sangre",
        "nivel de alcohol en la sangre",
    ],

    "alcohosensor": [
        "alcohosensor", "alcoholímetro",
        "detector de alcohol", "prueba de alcohol",
        "aparato de alcoholemia",
        "detector de alcohol portátil",
        "prueba de alcoholemia con aparato",
    ],

    "bicicleta": [
        "bici", "bicicleta", "ciclista",
        "en bici", "andar en bici",
        "movilidad sostenible",
        "bicicleta urbana",
        "bicicleta de montaña",
        "bicicleta de carretera",
    ],

    "casco": [
        "casco", "sin casco", "casco de moto",
        "casco protector", "casco para moto",
        "casco certificado",
        "casco de seguridad",
        "multa por no usar casco",
        "comparendo por no llevar casco",
        "casco abierto", "casco cerrado",
        "casco con visor", "casco sin visor",
        "casco talla correcta",
    ],

    "cinturon-de-seguridad": [
        "cinturón", "seguridad", "cinturón de seguridad",
        "no uso cinturón", "multa cinturón",
        "cinturón de seguridad obligatorio",
        "por qué usar cinturón",
        "cinturón de tres puntos",
        "cinturón trasero",
        "multa por no usar cinturón de seguridad",
    ],

    "comparendo": [
        "comparendo", "multa", "parte",
        "me pusieron comparendo", "recibir comparendo",
        "papeleta", "infracción",
        "qué es un comparendo",
        "comparendo de tránsito",
        "comparendo electrónico",
        "comparendo en sitio",
        "comparendo por fotomulta",
        "comparendo pedagógico",
        "tipos de comparendo",
        "comparendo y multa diferencia",
    ],

    "conductor": [
        "conductor", "manejar", "conducir",
        "chofer", "al volante",
        "quién es el conductor",
        "conductor responsable",
        "conductor del vehículo",
        "conductor ebrio",
        "conductor sin licencia",
        "conductor particular", "conductor profesional",
    ],

    "croquis": [
        "croquis", "dibujo del accidente",
        "cómo hacer un croquis", "parte de accidente",
        "croquis de accidente",
        "cómo dibujar un croquis",
        "croquis explicativo",
    ],

    "embriaguez": [
        "embriaguez", "borracho", "ebrio",
        "estado de embriaguez", "manejar ebrio",
        "qué es la embriaguez",
        "grados de embriaguez",
        "embriaguez alcohólica",
        "estado de embriaguez conductor",
        "manejar en estado de embriaguez",
        "sanciones por embriaguez",
    ],

    "grua": [
        "grúa", "se llevaron mi carro", "patios",
        "remolque", "inmovilización",
        "grúa de tránsito",
        "cuánto cobra la grúa",
        "tarifa grúa",
        "dónde está mi carro",
        "cómo recuperar el carro de la grúa",
        "grúa particular", "grúa oficial",
        "costo de grúa por inmovilización",
    ],

    "infraccion": [
        "infracción", "multa", "comparendo",
        "violación", "sanción",
        "qué es una infracción",
        "tipos de infracciones de tránsito",
        "infracciones leves", "infracciones graves",
        "infracciones muy graves",
        "clasificación de infracciones",
        "código de infracción",
    ],

    "inmovilizacion": [
        "inmovilización", "patios", "grúa",
        "se llevaron el carro", "inmovilizado",
        "inmovilización del vehículo",
        "cuándo inmovilizan un vehículo",
        "motivos de inmovilización",
        "patios cómo recuperar el carro",
        "costo de patios",
        "días en patios",
        "cómo sacar el carro de patios",
        "inmovilización por falta de documentos",
        "inmovilización por soat vencido",
        "inmovilización por revisión vencida",
        "inmovilización por embriaguez",
    ],

    "licencia-de-conduccion": [
        "licencia", "pase", "carnet",
        "licencia de conducción", "carné",
        "cómo sacar la licencia", "perder la licencia",
        "licencia vencida", "renovar licencia",
        "licencia de conducción colombiana",
        "licencia por primera vez",
        "licencia para moto", "licencia para carro",
        "licencia para taxi",
        "categorías de licencia",
        "licencia A1", "licencia A2",
        "licencia B1", "licencia B2",
        "licencia C1", "licencia C2",
        "licencia de tránsito",
        "revalidar licencia",
        "licencia extranjera en Colombia",
        "canje de licencia extranjera",
        "venció la licencia",
        "perdí la licencia", "renovación de licencia",
        "cada cuánto se renueva la licencia",
        "examen médico para licencia",
        "requisitos para licencia de conducción",
    ],

    "multa": [
        "multa", "comparendo", "sanción",
        "pagar multa", "cuánto vale la multa",
        "multa de tránsito",
        "tipos de multas",
        "multa por exceso de velocidad",
        "multa por semáforo",
        "multa por estacionamiento",
        "multa por documentos",
        "multa por embriaguez",
        "valor de las multas",
        "cuánto vale cada multa",
        "tabla de multas",
        "multas 2025", "multas 2026",
    ],

    "peaton": [
        "peatón", "caminar", "a pie",
        "cruzar la calle", "paso peatonal",
        "derechos del peatón",
        "deberes del peatón",
        "peatón en la vía",
        "cruzar por la esquina",
        "cruzar por el paso peatonal",
        "peatón imprudente",
        "atropellamiento de peatón",
        "multa al peatón",
        "comparendo para peatones",
    ],

    "semaforo": [
        "semáforo", "luz roja", "luz verde",
        "luz amarilla", "me pasé el semáforo",
        "semáforo peatonal",
        "semáforo vehicular",
        "semáforo en rojo qué significa",
        "semáforo intermitente",
        "semáforo dañado",
    ],

    "senal-de-transito": [
        "señal", "señal de tránsito",
        "pare", "ceda el paso", "señalización",
        "señal preventiva", "señal reglamentaria",
        "señal informativa",
        "señal vertical", "señal horizontal",
    ],

    "sobrecarga": [
        "sobrecarga", "exceso de carga",
        "capacidad de carga", "multa por sobrecarga",
        "exceso de peso",
        "peso bruto vehicular excedido",
        "comparendo por sobrecarga",
    ],

    "sobrecupo": [
        "sobrecupo", "exceso de pasajeros",
        "cupo", "cuántas personas caben",
        "multa por sobrecupo",
        "comparendo por exceso de pasajeros",
        "capacidad de pasajeros excedida",
        "bus con sobrecupo",
        "moto con sobrecupo",
    ],

    "transporte": [
        "transporte", "movilidad",
        "servicio público", "bus",
        "transporte en Colombia",
        "sistema de transporte",
    ],

    "reten": [
        "retén", "reten de tránsito",
        "control", "me pararon",
        "puesto de control",
        "qué hacer en un retén",
        "derechos en un retén",
        "reten de la policía",
        "reten de tránsito derechos",
        "me pararon en un retén",
        "paso por un retén",
        "cómo actuar en un retén",
        "reten militar", "reten policial",
    ],

    "retencion": [
        "retención", "retenido", "detención",
        "me retuvieron", "no me dejan ir",
        "retención del vehículo",
        "retención de la licencia",
        "retención de documentos",
        "retención ilegal",
    ],

    "ciclovia": [
        "ciclovía", "bicicleta", "dominical",
        "vía para bicicletas", "día sin carro",
        "ciclovía dominical Bogotá",
        "ciclorruta",
        "día sin carro y sin moto",
        "bicicleta en ciclovía",
    ],

    "matricula": [
        "matrícula", "registro", "placa",
        "cómo matricular un carro",
        "matrícula de vehículo",
        "registro automotor",
        "matrícula inicial",
        "traslado de matrícula",
        "cancelación de matrícula",
        "matrícula de moto",
        "matrícula de carro nuevo",
    ],

    # ========================================================
    # ARTÍCULOS ADICIONALES CUBIERTOS
    # ========================================================

    "accesibilidad": [
        "discapacidad", "discapacitado", "accesibilidad",
        "rampa", "silla de ruedas",
        "vehículo para discapacitados",
        "estacionamiento para discapacitados",
        "derechos de personas con discapacidad",
        "transporte para discapacitados",
        "pico y placa para discapacitados",
        "comparendo por ocupar espacio discapacitados",
        "multa por estacionar en zona de discapacitados",
    ],

    "cambio-de-servicio": [
        "cambio de servicio", "servicio público a particular",
        "particular a público", "transformar vehículo",
        "cambio de uso de vehículo",
        "vehículo de servicio particular",
        "vehículo de servicio público",
        "cambiar de servicio el carro",
        "requisitos cambio de servicio",
    ],

    "transformacion-de-vehiculo": [
        "transformación vehicular", "modificar carro",
        "modificar moto", "cambio de carrocería",
        "accesorios no originales",
        "espejos que no son de fábrica",
        "modificación de espejos",
        "espejos no originales moto",
        "rines modificados", "llantas no originales",
        "polarizado", "vidrios polarizados",
        "polarizado del carro", "cambiar color del carro",
        "pintura del carro diferente",
        "modificación de motor", "cambio de motor",
        "cambio de chasis", "modificación de chasis",
        "modificación de escape",
        "escape libre", "silenciador modificado",
        "parrilla para maletas", "parrilla para techo",
        "modificaciones autorizadas",
        "permiso para modificar vehículo",
        "multa por modificar el carro",
        "comparendo por modificación de vehículo",
        "modificar farolas", "farolas no originales",
        "modificación de luces", "farola modificada",
        "kit de carrocería", "body kit",
        "alerón", "spoiler",
        "tuning", "carro tuneado",
        "moto tuneada", "moto modificada estéticamente",
        "manillar alto moto", "manillar modificado moto",
        "asiento modificado moto",
        "moto con baúl", "baúl para moto",
        "moto con maletero",
        "guardaescobas modificado",
    ],

    "comparecencia-con-abogado": [
        "abogado", "defensa legal", "representación legal",
        "necesito un abogado",
        "abogado de tránsito",
        "consultar abogado",
        "abogado para comparendo",
        "defensa en multa de tránsito",
        "abogado especialista en tránsito",
        "tutela", "acción de tutela",
        "derecho de petición",
        "recurso legal", "apelar con abogado",
        "cárcel por accidente",
        "abogado para accidente de tránsito",
        "defensa penal tránsito",
    ],

    "embargo-vehiculos": [
        "embargo", "embargaron mi carro",
        "deuda", "cuota", "banco",
        "leasing", "crédito vehicular",
        "vehículo embargado",
        "me embargaron la moto",
        "embargo por multas",
        "embargo por deudas",
        "me quitaron el carro por deuda",
        "cómo evitar embargo",
        "levantamiento de embargo",
        "vehículo en prenda",
        "garantía vehicular",
    ],

    "comparendo-pedagogico": [
        "comparendo pedagógico",
        "curso pedagógico",
        "multa pedagógica",
        "educación vial en lugar de multa",
        "comparendo didáctico",
        "en lugar de multa un curso",
        "curso de seguridad vial",
        "comparendo sin pagar",
        "asistir a curso por comparendo",
    ],

    "amonestacion-y-reincidencia": [
        "reincidencia", "cometí la misma infracción",
        "segunda multa", "tercera multa",
        "multa repetida", "reincidente",
        "sanción por reincidencia",
        "aumento de sanción por repetir",
        "reincidencia en infracciones",
        "comparendo repetido",
    ],

    "aplicaion-de-otros-codigos-y-norma-aplicable": [
        "código penal", "código disciplinario",
        "código de comercio",
        "normas internacionales de tránsito",
        "tratados internacionales tránsito",
        "convención de tránsito",
        "normas complementarias",
    ],

    "sanciones-centros-ensenanza-automotriz": [
        "escuela de conducción", "autoescuela",
        "sanción a escuela de manejo",
        "instructor de manejo",
        "curso de conducción",
        "clases de manejo",
        "multa a escuela de conducción",
    ],

    "gradualidad-de-sanciones": [
        "gradualidad", "progresión de sanciones",
        "primera infracción", "primera vez",
        "reincidencia sanción más alta",
        "aumento progresivo de multas",
        "escala de sanciones",
    ],

    "notificacion-de-infracciones": [
        "notificación", "me notificaron",
        "cómo notifican una multa",
        "notificación personal",
        "notificación por correo",
        "notificación electrónica",
        "notificación de comparendo",
        "no me notificaron",
        "multa sin notificar",
        "notificación inválida",
        "error en notificación",
    ],

    "subsanar-infracciones-2": [
        "subsanación", "falla arreglable",
        "arreglé la falla", "corregí la infracción",
        "infracción corregible",
        "cómo subsanar",
        "60 minutos para subsanar",
        "subsanar comparendo",
    ],

    "procedimiento-para-comparendo-2": [
        "pasos del comparendo",
        "cómo funciona un comparendo",
        "comparendo paso a paso",
        "después del comparendo",
        "proceso de comparendo",
    ],

    "procedimiento-para-comparendo-3": [
        "cómo se aplica un comparendo",
        "el agente me puso comparendo",
        "comparendo manual",
        "comparendo automático",
    ],

    "informe-policial-de-accidente": [
        "IPAT", "informe policial",
        "informe de accidente",
        "denuncia del accidente",
        "atestado policial",
    ],

    "procedimiento-accidentes-danos-materiales": [
        "accidente solo daños",
        "choque sin heridos",
        "accidente sin lesionados",
        "daños materiales accidente",
        "solo daños",
    ],

    "cruce-e-interseccion": [
        "intersección", "cruce de vías",
        "cruce regulado", "cruce no regulado",
        "cruce con semáforo",
        "cruce sin semáforo",
        "glorieta",
        "rotonda",
    ],

    "paso-a-nivel": [
        "paso a nivel", "cruce ferroviario",
        "tren", "línea férrea",
        "cruce de tren",
        "paso de ferrocarril",
    ],

    "bocacalle": [
        "bocacalle", "esquina",
        "cruce de calles",
        "intersección de calles",
        "esquina de la calle",
    ],

    "sardinel": [
        "sardinel", "bordillo",
        "andén", "cuneta",
    ],

    "glorieta": [
        "glorieta", "rotonda",
        "cruce circular",
        "cómo manejar en glorieta",
        "quién tiene la vía en glorieta",
    ],

    "carretera": [
        "carretera", "autopista",
        "vía nacional", "vía intermunicipal",
        "carretera nacional",
    ],

    "autopista": [
        "autopista", "vía rápida",
        "carretera de alta velocidad",
    ],

    "via": [
        "vía", "calle", "carrera",
        "avenida", "carretera",
        "partes de la vía",
    ],

    "calzada": [
        "calzada", "parte de la vía",
        "superficie de rodadura",
    ],

    "carreteable": [
        "carreteable", "vía destapada",
        "vía sin pavimentar",
        "camino de tierra",
    ],

    "cuneta": [
        "cuneta", "drenaje de la vía",
        "canal de aguas",
    ],

    "homologacion": [
        "homologación", "homologar vehículo",
        "vehículo importado",
        "homologar moto",
        "requisitos de homologación",
    ],

    "tipo-de-carroceria": [
        "tipo de carrocería", "carrocería",
        "carrocería del vehículo",
        "clase de vehículo",
        "sedán", "camioneta",
        "SUV", "todo terreno",
        "pickup", "camión",
        "bus", "microbús",
        "motocicleta",
    ],

    "clase-de-vehiculo": [
        "clase de vehículo", "tipo de vehículo",
        "categoría vehicular",
        "vehículo automotor",
        "vehículo de tracción animal",
        "vehículo de pedal",
    ],

    "linea-de-vehiculo": [
        "línea de vehículo", "modelo del carro",
        "marca del carro",
        "año del vehículo",
        "referencia del vehículo",
    ],

    "placa": [
        "placa", "matrícula",
        "número de placa",
        "placa del carro",
        "placa de la moto",
        "placa única nacional",
        "sin placa",
        "placa provisional",
        "cambio de placa",
        "placa para moto",
    ],

    "ubicacion-de-placas": [
        "dónde va la placa",
        "ubicación de la placa",
        "placa delantera",
        "placa trasera",
        "placa mal ubicada",
        "multa por ubicación de placa",
    ],

    "registro-nacional-automotor": [
        "registro automotor",
        "RNA", "registro nacional",
        "registro del vehículo",
        "cómo registrar un vehículo",
    ],

    "centro-de-diagnostico-automotor": [
        "CDA", "centro de diagnóstico",
        "revisión técnico mecánica",
        "dónde hacer la revisión",
        "CDA autorizado",
        "centro de diagnóstico automotor",
    ],

    "licencia-de-transito": [
        "licencia de tránsito",
        "tarjeta de propiedad",
        "documento del vehículo",
        "papeles del carro",
        "certificado de tradición",
    ],

    "pequenos-remolques": [
        "remolque", "remolque pequeño",
        "trailer", "carro de carga",
        "remolque para moto",
        "remolque para carro",
    ],

    "semirremolques": [
        "semirremolque", "tractocamión",
        "mula", "camión con remolque",
        "vehículo articulado",
    ],

    "remolque": [
        "remolque", "remolcar",
        "vehículo de remolque",
        "grúa",
    ],

    "carroceria": [
        "carrocería", "carrocería del vehículo",
        "tipo de carrocería",
        "modificación de carrocería",
    ],

    "chasis": [
        "chasis", "bastidor",
        "número de chasis",
        "modificación de chasis",
        "cambio de chasis",
    ],

    "cabina": [
        "cabina", "cabina del vehículo",
        "cabina de pasajeros",
        "cabina de carga",
    ],

    "parqueadero": [
        "parqueadero", "estacionamiento",
        "aparcamiento",
        "zona de parqueo",
        "parqueadero público",
        "parqueadero privado",
    ],

    "agente-de-transito": [
        "agente de tránsito", "tránsito",
        "policía de tránsito",
        "agente vial",
        "autoridad de tránsito",
        "funcionario de tránsito",
        "tombo", "tránsito municipal",
        "agente de movilidad",
    ],

    "organismos-de-transito": [
        "secretaría de movilidad",
        "organismo de tránsito",
        "dirección de tránsito",
        "entidad de tránsito",
        "ministerio de transporte",
        "supertransporte",
        "autoridad de tránsito municipal",
        "secretaría de tránsito",
    ],
}


def load_yaml_frontmatter(content: str) -> dict[str, str]:
    """Extract fields from YAML frontmatter."""
    m = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not m:
        return {}
    return _parse_yaml_fields(m.group(1))


def _parse_yaml_fields(yaml: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in yaml.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('-'):
            key, _, val = line.partition(':')
            key = key.strip()
            # Handle in-line arrays [...]
            if val.strip().startswith('['):
                arr = val.strip()
                if arr == '[':
                    arr_lines = []
                    for rest_line in yaml.split('\n')[yaml.split('\n').index(line) + 1:]:
                        arr_lines.append(rest_line)
                        if ']' in rest_line:
                            break
                    arr = '\n'.join([arr] + arr_lines)
                fields[key] = arr
            else:
                fields[key] = val.strip()
    return fields


def extract_keyword_list(content: str) -> list[str]:
    m = re.search(r'keywords:\s*\[(.*?)\]', content, re.DOTALL)
    if not m:
        return []
    return [k.strip() for k in re.findall(r'"([^"]*)"', m.group(1)) if k.strip()]


def replace_keywords(content: str, existing: list[str], additions: list[str]) -> str:
    combined = list(dict.fromkeys(existing + additions))
    kw_lines = "[\n" + ",\n".join(f'  "{kw}"' for kw in combined) + ",\n]"
    return re.sub(
        r'keywords:\s*\[.*?\]',
        f'keywords: {kw_lines}',
        content,
        flags=re.DOTALL,
    )


def process_file(filepath: str):
    with open(filepath) as f:
        original = f.read()

    fields = load_yaml_frontmatter(original)
    article_id = fields.get('id', os.path.basename(filepath).replace('.md', '')).strip('"')

    existing = extract_keyword_list(original)
    additions = list(GENERIC_ADDITIONS)

    # Match by ID substring
    for pattern, kw_list in PATTERNS.items():
        if pattern in article_id:
            additions.extend(kw_list)

    # Match by title keywords
    titulo = fields.get('titulo', '').lower()
    for pattern, kw_list in PATTERNS.items():
        if pattern.replace('-', ' ') in titulo or pattern.replace('_', ' ') in titulo:
            additions.extend(kw_list)

    if not additions:
        return

    new_kws = [kw for kw in additions if kw not in existing]
    if not new_kws:
        return

    updated = replace_keywords(original, existing, new_kws)

    with open(filepath, 'w') as f:
        f.write(updated)

    old_count = len(existing)
    new_count = len(existing) + len(new_kws)
    print(f"  {article_id:50s} {old_count:3d} → {new_count:3d} keywords ({len(new_kws):+d})")


def main():
    files = []
    for root, dirs, names in os.walk(SRC):
        for name in names:
            if name.endswith('.md') and not name.startswith('TEMPLATE'):
                files.append(os.path.join(root, name))

    files.sort()
    print(f"Found {len(files)} files to process\n")

    count = 0
    for fp in files:
        process_file(fp)
        count += 1
        if count % 30 == 0:
            print(f"  ... {count}/{len(files)}")

    print(f"\nDone! Processed {count} files.")


if __name__ == "__main__":
    main()
