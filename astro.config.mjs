/**
 * ARCHIVO: astro.config.mjs
 *
 * PROPÓSITO:
 *   Configuración principal de Astro.
 *   Define integraciones (React), modo de renderizado (SSR)
 *   y adaptador de despliegue (Node standalone).
 *
 * CÓMO MODIFICAR:
 *   - Para agregar una integración: añadir al array `integrations`
 *   - Para cambiar a modo estático: cambiar `output: "server"` por `output: "static"` y quitar adapter
 *   - Para desplegar en Vercel/Netlify: cambiar adapter por @astrojs/vercel o @astrojs/netlify
 */

// @ts-check
import { defineConfig } from "astro/config";

import node from "@astrojs/node";

import react from "@astrojs/react";

import tailwindcss from "@tailwindcss/vite";

// https://astro.build/config
export default defineConfig({
  integrations: [react()],
  output: "server",
  adapter: node({ mode: "standalone" }),

  vite: {
    plugins: [tailwindcss()],
  },
});
