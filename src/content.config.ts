/**
 * ARCHIVO: src/content.config.ts
 *
 * PROPÓSITO:
 *   Define el schema (forma) que deben tener los archivos .md
 *   dentro de src/content/. Cada subcarpeta es una "colección"
 *   (abusos, normas-comportamiento, definiciones, etc.).
 *   Astro usa esto para validar los frontmatter y dar
 *   autocompletado en TypeScript.
 *
 * ESTRUCTURA:
 *   - Cada colección usa `defineCollection()` con un schema Zod.
 *   - `schema`: schema estricto para contenido principal (todos los campos).
 *   - `defSchema`: schema flexible para definiciones (varios campos opcionales).
 *   - `export const collections`: mapea cada subcarpeta a su schema.
 *   - Cada colección tiene su propio glob apuntando solo a su carpeta
 *     para evitar que los .md de una colección se validen contra el schema de otra.
 *
 * CÓMO MODIFICAR:
 *   - Para agregar un campo nuevo a los .md:
 *     1. Agregar el campo al frontmatter de cada .md
 *     2. Agregar el campo aquí en el schema correspondiente
 *   - Para agregar una carpeta nueva a content/:
 *     1. Crear la carpeta con sus .md
 *     2. Agregar la colección aquí en `export const collections`
 *   - Para convertir un campo en opcional: agregar .optional()
 *   - Para cambiar el tipo de un campo: cambiar z.string() por z.number(), etc.
 */

import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";

const schema = z.object({
  id: z.string(),
  tipo: z.string(),
  numero: z.string().nullable(),
  titulo: z.string(),
  texto_simple: z.string(),
  categoria: z.string(),
  subcategoria: z.string(),
  severidad: z.string().nullable(),
  codigo_infraccion: z.string().nullable(),
  sancion: z
    .union([
      z.object({
        valor_smdlv: z.number().optional(),
        inmovilizacion: z.boolean().optional(),
      }),
      z.string(),
    ])
    .nullable(),
  keywords: z.array(z.string()),
  articulos_relacionados: z.array(z.string()),
  aplica_a: z.array(z.string()),
  referencias_legales: z.array(z.string()),
  vigencia: z.object({
    estado: z.string(),
    ultima_revision: z.string(),
    nota: z.string(),
  }),
  fuente_oficial: z.object({
    tipo: z.string(),
    referencia: z.string(),
    url: z.string().url().refine(
      (u) => u.startsWith("http://") || u.startsWith("https://"),
      "Solo URLs HTTP/HTTPS permitidas"
    ),
  }),
});

const defSchema = z.object({
  id: z.string(),
  tipo: z.string(),
  titulo: z.string(),
  texto_simple: z.string(),
  keywords: z.array(z.string()),
  numero: z.string().nullable().optional(),
  categoria: z.string().optional(),
  subcategoria: z.string().optional(),
  severidad: z.string().nullable().optional(),
  codigo_infraccion: z.string().nullable().optional(),
  sancion: z
    .union([
      z.object({
        valor_smdlv: z.number().optional(),
        inmovilizacion: z.boolean().optional(),
      }),
      z.string(),
    ])
    .nullable()
    .optional(),
  articulos_relacionados: z.array(z.string()).optional(),
  aplica_a: z.array(z.string()).optional(),
  referencias_legales: z.array(z.string()).optional(),
  vigencia: z
    .object({
      estado: z.string(),
      ultima_revision: z.string(),
      nota: z.string(),
    })
    .optional(),
  fuente_oficial: z
    .object({
      tipo: z.string(),
      referencia: z.string(),
      url: z.string().url().refine(
        (u) => u.startsWith("http://") || u.startsWith("https://"),
        "Solo URLs HTTP/HTTPS permitidas"
      ),
    })
    .optional(),
});

export const collections = {
  abusos: defineCollection({
    loader: glob({ pattern: "abusos/**/*.md", base: "./src/content" }),
    schema,
  }),
  alcoholemia: defineCollection({
    loader: glob({ pattern: "alcoholemia/**/*.md", base: "./src/content" }),
    schema,
  }),
  definiciones: defineCollection({
    loader: glob({ pattern: "definiciones/**/*.md", base: "./src/content" }),
    schema: defSchema,
  }),
  derechos: defineCollection({
    loader: glob({ pattern: "derechos/**/*.md", base: "./src/content" }),
    schema,
  }),
  "disposiciones-finales": defineCollection({
    loader: glob({
      pattern: "disposiciones-finales/**/*.md",
      base: "./src/content",
    }),
    schema,
  }),
  "infracciones-131": defineCollection({
    loader: glob({
      pattern: "infracciones-131/**/*.md",
      base: "./src/content",
    }),
    schema,
  }),
  "leyes-complementarias": defineCollection({
    loader: glob({
      pattern: "leyes-complementarias/**/*.md",
      base: "./src/content",
    }),
    schema,
  }),
  "normas-comportamiento": defineCollection({
    loader: glob({
      pattern: "normas-comportamiento/**/*.md",
      base: "./src/content",
    }),
    schema,
  }),
  "normas-sanciones": defineCollection({
    loader: glob({
      pattern: "normas-sanciones/**/*.md",
      base: "./src/content",
    }),
    schema,
  }),
  procedimientos: defineCollection({
    loader: glob({ pattern: "procedimientos/**/*.md", base: "./src/content" }),
    schema,
  }),
};
