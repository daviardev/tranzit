import { getCollection } from "astro:content";

import Fuse from "fuse.js";

import { searchEmbeddings } from "@/lib/embeddings";
import type { LawEntry, ArticleResult } from "@/lib/types";
import { COLLECTIONS } from "@/lib/types";

type SearchableDoc = {
  id: string;
  titulo: string;
  texto_simple: string;
  keywords: string[];
  codigo_infraccion: string | null;
  numero: string | null;
  aplica_a: string[];
  coleccion: string;
  slug: string;
};

const FUSE_KEYS: { name: keyof SearchableDoc; weight: number }[] = [
  { name: "titulo", weight: 0.35 },
  { name: "keywords", weight: 0.35 },
  { name: "texto_simple", weight: 0.2 },
  { name: "codigo_infraccion", weight: 0.1 },
];

let fuse: Fuse<SearchableDoc> | null = null;
let entryMap: Map<string, LawEntry> = new Map();
let docs: SearchableDoc[] = [];

async function buildIndex(): Promise<Fuse<SearchableDoc>> {
  if (fuse) return fuse;

  for (const name of COLLECTIONS) {
    const entries = await getCollection(name);
    for (const entry of entries) {
      const data = entry.data as LawEntry;
      const doc: SearchableDoc = {
        id: data.id,
        titulo: data.titulo,
        texto_simple: data.texto_simple,
        keywords: data.keywords ?? [],
        codigo_infraccion: data.codigo_infraccion,
        numero: data.numero,
        aplica_a: data.aplica_a ?? [],
        coleccion: name,
        slug: `/${name}/${data.id}`,
      };
      docs.push(doc);

      entryMap.set(data.id, data);
    }
  }

  fuse = new Fuse<SearchableDoc>(docs, {
    keys: FUSE_KEYS,
    threshold: 1.0,
    includeScore: true,
    minMatchCharLength: 3,
  });

  return fuse;
}

function toArticleResult(id: string): ArticleResult | null {
  const mapped = entryMap.get(id);
  if (!mapped) return null;
  const doc = docs.find((d) => d.id === id);
  if (!doc) return null;
  return {
    id: mapped.id,
    titulo: mapped.titulo,
    texto_simple: mapped.texto_simple,
    codigo_infraccion: mapped.codigo_infraccion ?? null,
    sancion: mapped.sancion ?? null,
    numero: mapped.numero ?? null,
    aplica_a: mapped.aplica_a ?? [],
    referencias_legales: mapped.referencias_legales ?? [],
    articulos_relacionados: mapped.articulos_relacionados ?? [],
    vigencia: mapped.vigencia ?? null,
    fuente_oficial: mapped.fuente_oficial ?? null,
    slug: doc.slug,
  };
}

export async function search(query: string): Promise<ArticleResult[]> {
  const normalized = query.toLowerCase().trim();

  // Always build the index first to populate entryMap
  await buildIndex();

  if (normalized.length < 2) {
    const all = docs.slice(0, 3);
    return all.map((d) => toArticleResult(d.id)).filter(Boolean);
  }

  // 1. Embeddings search (semantic)
  try {
    const ids = await searchEmbeddings(normalized, 5);
    const results = ids.map((id) => toArticleResult(id)).filter(Boolean);
    if (results.length > 0) {
      console.log("[Search] Embeddings:", results.map((r) => r.id).join(", "));
      return results;
    }
  } catch (e) {
    console.error("[Search] Embeddings error:", e);
  }

  // 2. Fallback: fuse
  const fuseResults = fuse!.search(normalized);
  const results = fuseResults.slice(0, 5).map((r) => toArticleResult(r.item.id)).filter(Boolean);
  console.log("[Search] Fuse fallback:", results.map((r) => r.id).join(", "));
  return results;
}
