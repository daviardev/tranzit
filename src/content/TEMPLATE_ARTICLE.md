---
# ─── IDENTIFICACIÓN ───
id: "art-131-b03"                # formato: art-<numero>-<literal>
tipo: "infraccion"               # infraccion | derecho | procedimiento | abuso | norma | null
numero: "131"                    # número de artículo en la ley
literal: "B.3"                   # literal exacto (si aplica)

# ─── TÍTULO ───
titulo: "Título claro y corto en lenguaje ciudadano"

# ─── EXPLICACIONES ───
texto_simple: "Explicación en lenguaje claro. Máx 1-2 frases. Sin jerga legal."

# ─── CLASIFICACIÓN ───
categoria: "infracciones"        # agrupación general
subcategoria: "documentos"       # agrupación específica
severidad: "grave"               # leve | grave | muy_grave | informativa (solo para tipo norma sin sanción)
codigo_infraccion: "B"           # A | B | C | D | E (según art. 131)

# ─── SANCIÓN ───
sancion:
  tipo: "mixta"                  # multa | inmovilizacion | suspension | mixta
  valor_smdlv: 8                 # solo el número. backend calcula el peso actualizado.
  inmovilizacion: true
  suspension_licencia: false
  descuento_pronto_pago: 0.5     # 0.5 = 50% de descuento

# ─── BÚSQUEDA (de esto vive el motor de búsqueda) ───
keywords:
  - "palabra clave exacta 1"
  - "palabra clave exacta 2"

sinonimos:
  - "forma coloquial de decirlo 1"
  - "forma coloquial de decirlo 2"

situaciones:
  - "ejemplo de situación real como la describiría un ciudadano"
  - "otro ejemplo cotidiano en jerga de calle"

# ─── RELACIONES ───
articulos_relacionados:
  - "art-127"
  - "art-55"
  - "art-82"

aplica_a:
  - "conductor"
  - "propietario"

# ─── REFERENCIAS LEGALES ───
referencias_legales:
  - "Ley 769 de 2002"
  - "Ley 1383 de 2010"

# ─── VIGENCIA ───
vigencia:
  estado: "vigente"              # vigente | derogado | modificado
  ultima_revision: "2026-03-26"
  nota: "El valor de la multa se actualiza según el SMDLV del año vigente."

# ─── FUENTE ───
fuente_oficial:
  tipo: "norma"
  referencia: "Código Nacional de Tránsito Terrestre"
  url: ""
---

## Texto oficial

(Pega aquí el texto legal exacto del artículo, literal o resolución.)

## Explicación ciudadana

(Explica en lenguaje claro: qué pasó, por qué aplica, cuál es la consecuencia principal.)

## Urgente ❗

(Qué debe hacer el ciudadano AHORA MISMO. Acción inmediata que no puede ignorar.)

## Qué hacer

- Paso concreto 1 (ej: "Verifica que el comparendo tenga el literal correcto")
- Paso concreto 2 (ej: "Toma fotos de las placas antes de modificarlas")
- Tienes 5 días hábiles para impugnar si consideras que fue mal impuesto
- Si pagas en los primeros 5 días hábiles, tienes derecho al 50% de descuento

## Qué no hacer ❌

- Error común 1 que agrava la situación
- Error común 2
- No firmes el comparendo si los datos son incorrectos
- No ignore el comparendo pensando que "se borra solo"

## Alerta ⚠️

(Cuándo necesita consultar con un abogado. Casos donde la situación es más grave de lo que parece o hay reincidencia.)

## Notas

- El valor de la multa en pesos se calcula automáticamente según el SMDLV vigente al momento de la infracción.
- Aplica en todo el territorio nacional, salvo que se especifique lo contrario.
- Esta información es orientativa. No reemplaza la asesoría de un abogado.
