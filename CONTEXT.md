# Contexto del Proyecto: Tranzit

## Visión
Tranzit es una aplicación web tipo LegalTech para Colombia. Su objetivo es ayudar a los ciudadanos en momentos de estrés (ej. retenes o comparendos) traduciendo situaciones cotidianas en artículos específicos de la Ley 769 de 2002 (Código Nacional de Tránsito).

## Búsqueda
- **Siempre devuelve candidatos:** El endpoint `/api/search` responde con `{ candidates: ArticleResult[] }` (top 5). Nunca devuelve "no se encontraron artículos".
- **Embeddings (primary):** `multilingual-e5-small` via `@xenova/transformers`. Los 241 artículos tienen sus embeddings pre-computados en `src/data/embeddings.json`. La query del usuario se embeddea en runtime (prefijo `query: `), cosine similarity contra los vectores pre-computados (prefijo `passage: `). Devuelve top 5. Ver `src/lib/embeddings.ts`.
- **Fuse.js (fallback):** Si embeddings falla (error), se usa Fuse.js con threshold 1.0, minMatchCharLength 3, keys: titulo (0.35), keywords (0.35), texto_simple (0.2), codigo_infraccion (0.1). Siempre devuelve top 5. Ver `src/lib/search.ts`.

## Keywords
Cada artículo tiene keywords coloquiales enriquecidos que permiten match con queries cotidianas. 241 artículos promedian ~30 keywords cada uno (desde scripts/enrich-keywords.py). Los keywords incluyen slang colombiano ("tombo", "lucas", "coima", "plata", "patios", "grúa", "pase", "sofá", "pico y placa", "fotomulta", etc).

## Estructura de Datos
Los datos legales se extraen de archivos Markdown locales en `src/content/`. Cada archivo sigue frontmatter YAML con:
- `id`, `titulo`, `texto_simple`, `keywords` (array de strings coloquiales)
- `codigo_infraccion`, `sancion`, `numero` (artículo legal)
- `aplica_a`, `referencias_legales`, `articulos_relacionados`
- `vigencia`, `fuente_oficial`

## Files relevantes
- `src/lib/search.ts`: embeddings primary → Fuse fallback → `ArticleResult[]`
- `src/pages/api/search.ts`: POST endpoint → `{ candidates }`
- `src/components/Launcher.tsx`: input + lista de candidatos
- `src/lib/embeddings.ts`: carga embeddings.json, pipeline multilingual-e5-small, cosine similarity → top 5
- `scripts/enrich-keywords.py`: agrega keywords coloquiales a todos los .md
- `scripts/generate-embeddings.mjs`: pre-computa embeddings en build

## UI
- Sin Tailwind, sin Framer Motion — HTML básico sin estilos
- Launcher muestra hasta 5 artículos como tarjetas con link "Ver artículo completo"
- Cada artículo tiene su página en `[...slug].astro` con `render(entry)` de astro:content
