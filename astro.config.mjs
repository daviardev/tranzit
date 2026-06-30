/**
 * ARCHIVO: astro.config.mjs
 *
 * PROPÓSITO:
 *   Configuración principal de Astro.
 *   Define integraciones (React), modo de renderizado (SSR)
 *   y adaptador de despliegue (Vercel).
 *
 * CÓMO MODIFICAR:
 *   - Para agregar una integración: añadir al array `integrations`
 *   - Para cambiar a modo estático: cambiar `output: "server"` por `output: "static"` y quitar adapter
 *   - Para desplegar en otra plataforma: cambiar adapter por @astrojs/node, @astrojs/netlify, etc.
 */

// @ts-check
import { defineConfig } from "astro/config";

import vercel from "@astrojs/vercel";

import react from "@astrojs/react";

import rehypeSanitize from "rehype-sanitize";

// https://astro.build/config
export default defineConfig({
  integrations: [react()],
  output: "server",
  adapter: vercel(),
  markdown: {
    rehypePlugins: [rehypeSanitize],
  },
});
