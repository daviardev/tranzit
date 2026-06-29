import { getCollection } from "astro:content";

import Fuse, { type FuseResult } from "fuse.js";

import { interpretQuery } from "@/lib/gemini";
import type { LawEntry, SearchableDoc, SearchResultItem, SearchResponse } from "@/lib/types";
import { COLLECTIONS } from "@/lib/types";

const FUSE_THRESHOLD = 0.4;
const POOR_RESULT_THRESHOLD = 3;

const FUSE_KEYS: { name: keyof SearchableDoc; weight: number }[] = [
  { name: "titulo", weight: 0.4 },
  { name: "keywords", weight: 0.3 },
  { name: "codigo_infraccion", weight: 0.15 },
  { name: "texto_simple", weight: 0.15 },
];

let fuse: Fuse<SearchableDoc> | null = null;

async function buildIndex(): Promise<Fuse<SearchableDoc>> {
  if (fuse) return fuse;

  const docs: SearchableDoc[] = [];

  for (const name of COLLECTIONS) {
    const entries = await getCollection(name);
    for (const entry of entries) {
      const data = entry.data as LawEntry;
      docs.push({
        id: data.id,
        titulo: data.titulo,
        texto_simple: data.texto_simple,
        keywords: data.keywords ?? [],
        codigo_infraccion: data.codigo_infraccion,
        coleccion: name,
        slug: `/${name}/${entry.id.replace(/\.md$/, "").replace(`${name}/`, "")}`,
      });
    }
  }

  fuse = new Fuse<SearchableDoc>(docs, {
    keys: FUSE_KEYS,
    threshold: FUSE_THRESHOLD,
    includeScore: true,
    minMatchCharLength: 2,
  });

  return fuse;
}

function toResultItems(
  results: FuseResult<SearchableDoc>[],
): SearchResultItem[] {
  return results
    .filter((r) => r.score !== undefined && r.score <= FUSE_THRESHOLD)
    .sort((a, b) => (a.score ?? 1) - (b.score ?? 1))
    .map((r) => ({
      ...r.item,
      score: r.score ?? 1,
    }));
}

export async function search(query: string): Promise<SearchResponse> {
  const normalized = query.toLowerCase().trim();
  if (normalized.length < 2) {
    return {
      results: [],
      explanation: null,
      keywords: [],
      source: "fuse-direct",
    };
  }

  const f = await buildIndex();

  // Paso 1: fuse.js directo
  let results = f.search(normalized);
  let goodResults = toResultItems(results);

  if (goodResults.length >= POOR_RESULT_THRESHOLD) {
    return {
      results: goodResults,
      explanation: null,
      keywords: [],
      source: "fuse-direct",
    };
  }

  // Paso 2: Gemini interpreta
  const geminiResult = await interpretQuery(normalized);
  const keywordQuery =
    geminiResult.keywords.length > 0
      ? geminiResult.keywords.join(" ")
      : normalized;

  // Paso 3: fuse.js con keywords de Gemini
  results = f.search(keywordQuery);
  goodResults = toResultItems(results);

  return {
    results: goodResults,
    explanation: geminiResult.explanation,
    keywords: geminiResult.keywords,
    source: "gemini-enhanced",
  };
}
