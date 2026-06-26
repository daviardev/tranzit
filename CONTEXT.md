# Contexto del Proyecto: Tranzit

## Visión
Tranzit es una aplicación web tipo LegalTech para Colombia. Su objetivo es ayudar a los ciudadanos en momentos de estrés (ej. retenes o comparendos) traduciendo situaciones cotidianas en artículos específicos de la Ley 769 de 2002 (Código Nacional de Tránsito).

## UI/UX Framework
- **Diseño:** Inspirado en la interfaz de "Notebooks" de Gemini (minimalista, tipografía grande, caja de contexto inferior).
- **Interactividad:** Tipo "Launcher" (búsqueda reactiva, sugerencias inline, transiciones fluidas de estado 'searching' a 'results').
- **Tecnología:** React, Tailwind CSS, Framer Motion (para animaciones spring).

## Estructura de Datos
Los datos legales se extraen de archivos Markdown locales en `src/data/transit-laws/`. Cada archivo sigue esta estructura:
- Título/Infracción
- Código/Artículo y Sanción
- Lista de verificación ("Qué verificar")
- Protocolo de conducta ("Qué no hacer")
