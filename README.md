
# Tranzit

**Traduce tu situación de tránsito a artículos de la Ley 769 de 2002.**

Tranzit es una aplicación LegalTech colombiana que ayuda a ciudadanos en momentos de estrés (retenes, comparendos) traduciendo situaciones cotidianas en lenguaje coloquial a artículos específicos del Código Nacional de Tránsito (Ley 769 de 2002).

> **Disclaimer:** Esta herramienta es informativa y no constituye asesoría legal. Siempre consulta con un abogado para tu caso específico.

---

## Demo

[🌐 tranzit-col.vercel.app](https://tranzit-col.vercel.app/)

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Framework | [Astro 7](https://astro.build) (SSR) |
| Frontend | React 19 + TypeScript |
| Styling | CSS plano (sin Tailwind, sin Framer Motion) |
| Search (primary) | Embeddings semánticos con `multilingual-e5-small` |
| Search (fallback) | Fuse.js (búsqueda difusa) |
| SEO | SSR dinámico, `render(entry)` desde Content Collections |
| Deployment | Vercel (serverless functions) |

---

## ¿Cómo funciona?

```
Usuario escribe: "un tombo me pidió plata para no multarme"
         │
         ▼
  1. Embeddings: multilingual-e5-small
     └─ Cosine similarity contra 241 vectores pre-computados
     └─ Prefijo "query:" para la búsqueda, "passage:" para documentos
     └─ Devuelve top 5 IDs
         │
         ├── ✅ Éxito → 5 artículos por similitud semántica
         │
         └── ❌ Error → Fallback Fuse.js
                        └─ threshold 1.0, minMatchCharLength 3
                        └─ keys: titulo(0.35), keywords(0.35),
                                  texto_simple(0.2), codigo_infraccion(0.1)
                        └─ Siempre devuelve top 5
```

- **Nunca** se muestra "no se encontraron artículos". Siempre hay 5 candidatos.
- Los embeddings se pre-computan en build (`scripts/generate-embeddings.mjs`) y se guardan en `src/data/embeddings.json` (~1.5MB, 384 dimensiones por vector).
- En runtime solo se embeddea la query del usuario (~300ms cold start, modelo cacheado en RAM).

---

## Estructura del proyecto

```
tranzit/
├── astro.config.mjs          # Configuración Astro (Vercel adapter, React, rehype-sanitize)
├── package.json
├── tsconfig.json
├── vercel.json               # Configuración de deploy
├── scripts/
│   ├── generate-embeddings.mjs   # Pre-computa embeddings en build
│   └── enrich-keywords.py        # Enriquece keywords coloquiales en artículos .md
├── public/
│   ├── favicon.ico
│   └── favicon.svg
└── src/
    ├── content.config.ts      # Schema Zod para validar frontmatter de artículos
    ├── components/
    │   └── Launcher.tsx       # Componente React: input + lista de candidatos
    ├── content/               # 241 artículos en Markdown (10 colecciones)
    │   ├── abusos/
    │   ├── alcoholemia/
    │   ├── definiciones/
    │   ├── derechos/
    │   ├── disposiciones-finales/
    │   ├── infracciones-131/
    │   ├── leyes-complementarias/
    │   ├── normas-comportamiento/
    │   ├── normas-sanciones/
    │   └── procedimientos/
    ├── data/
    │   └── embeddings.json    # Vectores pre-computados (generado en build)
    ├── layouts/
    │   └── BaseLayout.astro
    ├── lib/
    │   ├── embeddings.ts      # Runtime: carga embeddings.json, pipeline E5, cosine similarity
    │   ├── sancion.ts         # Helper: formato legible para sanciones ({SMLDV + inmovilización})
    │   ├── search.ts          # Orquestador: embeddings primary → Fuse fallback
    │   └── types.ts           # Tipos compartidos (LawEntry, ArticleResult, COLLECTIONS)
    ├── pages/
    │   ├── index.astro        # Página principal con <Launcher client:load />
    │   ├── [...slug].astro    # SSR dinámico: renderiza artículo por slug
    │   └── api/search.ts      # Endpoint POST /api/search → { candidates }
    └── styles/
        └── global.css         # Estilos globales
```

---

## Convenciones del proyecto

### Contenido (artículos .md)

Cada artículo en `src/content/` sigue este frontmatter YAML:

```yaml
---
id: "slug-del-articulo"
tipo: "articulo" | "definicion" | "procedimiento"
numero: "131" | null
titulo: "Normas de comportamiento"
texto_simple: "Resumen breve del artículo..."
categoria: "Normas de comportamiento"
subcategoria: "Conducción"
severidad: "leve" | "grave" | null
codigo_infraccion: "C29" | null
sancion:
  valor_smdlv: 30        # número, o
  inmovilizacion: true   # booleano, o
                         # string directo, o null
keywords:
  - "slang colombiano"
  - "palabras clave"
  - "términos coloquiales"
articulos_relacionados:
  - "id-de-otro-articulo"
aplica_a:
  - "Conductores"
  - "Peatones"
referencias_legales:
  - "Ley 769 de 2002, Artículo 131"
vigencia:
  estado: "Vigente"
  ultima_revision: "2024-01-15"
  nota: "Modificado por Ley 1234 de 2023"
fuente_oficial:
  tipo: "Ley"
  referencia: "Ley 769 de 2002"
  url: "https://..."
---
```

**Reglas:**
- `id` debe coincidir con el nombre del archivo (sin `.md`)
- `keywords` debe incluir slang colombiano relevante (ej. "tombo", "lucas", "patios", "grúa", "pase")
- `texto_simple` es un resumen del artículo en lenguaje ciudadano
- `url` en `fuente_oficial` debe ser HTTP/HTTPS válida (validado por Zod en build)
- Las sanciones pueden ser un objeto `{ valor_smdlv, inmovilizacion }`, un string, o `null`
- No uses `"MISSING"` como placeholder para sanciones (se trata como null)

### Código

- Sin Tailwind CSS ni Framer Motion — solo CSS plano o módulos
- Comentarios al inicio de cada archivo explicando propósito y cómo modificarlo
- TypeScript estricto en toda la app
- Los archivos de contenido (`.md`) no tienen comentarios de código
- `scripts/` contiene herramientas auxiliares (Python/MJS) que no forman parte del runtime

---

## Desarrollo local

### Prerrequisitos

- Node.js 22.x
- pnpm 10+

### Instalación

```bash
pnpm install
```

### Desarrollo

```bash
pnpm dev
# → http://localhost:4321
```

### Build

```bash
pnpm build
```

El build ejecuta dos pasos:
1. `node scripts/generate-embeddings.mjs` — genera `src/data/embeddings.json`
2. `astro build` — build SSR con output para Vercel (`.vercel/output/`)

### Preview

```bash
pnpm preview
```

---

## Scripts disponibles

| Comando | Descripción |
|---------|------------|
| `pnpm dev` | Servidor de desarrollo con hot-reload |
| `pnpm build` | Genera embeddings + build de producción |
| `pnpm preview` | Previsualiza el build local |
| `node scripts/generate-embeddings.mjs` | Regenera embeddings después de modificar artículos |
| `python3 scripts/enrich-keywords.py` | Re-enriquece keywords después de agregar/quitar artículos |

---

## ¿Cómo contribuir?

### Pull Requests

1. **Fork** el repositorio.
2. Crea una rama descriptiva: `feat/nueva-funcionalidad` o `fix/error-x`.
3. Haz cambios pequeños y enfocados. Prefiere varios PRs pequeños sobre uno grande.
4. Asegura que el build pase: `pnpm build`.
5. Si agregas o modificas contenido (artículos .md):
   - Sigue el formato YAML descrito arriba.
   - Ejecuta `python3 scripts/enrich-keywords.py` para mantener keywords consistentes.
   - Ejecuta `node scripts/generate-embeddings.mjs` para regenerar embeddings.
6. Envía el PR contra `main`.

### Issues

- Usa issues para reportar bugs, sugerir keywords faltantes, o proponer funcionalidades.
- Para keywords faltantes: incluye la situación coloquial que no encontró resultados y qué artículo esperabas.

### Pautas

- **Mantén la estructura de carpetas**. `content/` se organiza por categorías legales.
- **No agregues Tailwind, Framer Motion, ni dependencias externas pesadas** sin discusión previa.
- **Nunca devuelvas "sin resultados"**. Siempre debe haber 5 candidatos (por embeddings o Fuse).
- **No muestres scores de relevancia** al usuario.
- **No uses APIs externas** para búsqueda (Gemini fue eliminado intencionalmente).

---

## Licencia

GNU General Public License v3.0 — [LICENSE](./LICENSE)
