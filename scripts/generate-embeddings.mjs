/**
 * GENERATE-EMBEDDINGS.MJS
 * =======================
 * Genera embeddings semánticos para todos los artículos.
 * Se ejecuta como pre-build: node scripts/generate-embeddings.mjs
 *
 * Salida: src/data/embeddings.json (array de { id, embedding })
 *
 * Cada embedding se genera del texto combinado:
 *   titulo + " " + texto_simple + " " + keywords.join(" ")
 *
 * CÓMO MODIFICAR:
 *   - Para cambiar el modelo: editar MODEL_NAME
 *   - Para cambiar el texto a embedder: editar buildText()
 */

import { pipeline } from "@xenova/transformers";
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SRC = join(__dirname, "..", "src", "content");
const OUT = join(__dirname, "..", "src", "data", "embeddings.json");
const MODEL = "Xenova/multilingual-e5-small";

function parseMd(filepath) {
  const raw = readFileSync(filepath, "utf-8");
  const m = raw.match(/^---\n(.*?)\n---/s);
  if (!m) return null;
  const yaml = m[0];
  const id = yaml.match(/id:\s*"([^"]+)"/)?.[1] ?? "";
  const titulo = yaml.match(/titulo:\s*"([^"]+)"/)?.[1] ?? "";
  const texto = yaml.match(/texto_simple:\s*"([^"]+)"/)?.[1] ?? "";
  const kwMatch = yaml.match(/keywords:\s*\[(.*?)\]/s);
  const keywords = kwMatch
    ? [...kwMatch[1].matchAll(/"([^"]+)"/g)].map((m) => m[1])
    : [];
  return { id, titulo, texto, keywords };
}

function buildText(article) {
  const kw = (article.keywords ?? []).join(" ");
  return `passage: ${article.titulo}. ${article.texto} ${kw}`.toLowerCase();
}

async function main() {
  console.log("Loading model...");
  const extract = await pipeline("feature-extraction", MODEL);
  console.log("Model ready");

  const files = [];
  function walk(dir) {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.name.endsWith(".md") && !entry.name.startsWith("TEMPLATE"))
        files.push(full);
    }
  }
  walk(SRC);
  console.log(`Found ${files.length} articles`);

  const articles = files.map(parseMd).filter(Boolean);
  const results = [];

  for (let i = 0; i < articles.length; i++) {
    const a = articles[i];
    const text = buildText(a);
    const output = await extract(text, { pooling: "mean", normalize: true });
    const embedding = Array.from(output.data);
    results.push({ id: a.id, embedding });
    if ((i + 1) % 50 === 0) console.log(`  ... ${i + 1}/${articles.length}`);
  }

  console.log(`Generated ${results.length} embeddings (dim=${results[0].embedding.length})`);

  const outDir = dirname(OUT);
  if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });
  writeFileSync(OUT, JSON.stringify(results));
  console.log(`Saved to ${OUT}`);
}

main().catch(console.error);
