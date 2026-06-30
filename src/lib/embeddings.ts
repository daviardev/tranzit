import { pipeline, type FeatureExtractionPipeline } from "@xenova/transformers";

import embeddingsData from "@/data/embeddings.json";

type EmbeddingEntry = {
  id: string;
  embedding: number[];
};

const MODEL = "Xenova/multilingual-e5-small";
const index: EmbeddingEntry[] = embeddingsData as EmbeddingEntry[];

let extractor: FeatureExtractionPipeline | null = null;

function cosineSimilarity(a: number[], b: number[]): number {
  let dot = 0,
    na = 0,
    nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return dot / (Math.sqrt(na) * Math.sqrt(nb));
}

async function getExtractor(): Promise<FeatureExtractionPipeline> {
  if (!extractor) {
    extractor = await pipeline("feature-extraction", MODEL) as FeatureExtractionPipeline;
  }
  return extractor;
}

export async function searchEmbeddings(
  query: string,
  topK = 5,
): Promise<string[]> {
  const ext = await getExtractor();
  const prefixed = `query: ${query}`;
  const output = await ext(prefixed, { pooling: "mean", normalize: true });
  const qVec = Array.from(output.data) as number[];

  const scored = index
    .map((entry) => ({
      id: entry.id,
      score: cosineSimilarity(qVec, entry.embedding),
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);

  return scored.map((s) => s.id);
}
