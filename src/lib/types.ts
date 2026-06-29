export type LawEntry = {
  id: string;
  tipo: string;
  numero: string | null;
  titulo: string;
  texto_simple: string;
  categoria: string;
  subcategoria: string;
  severidad: string | null;
  codigo_infraccion: string | null;
  sancion: unknown;
  keywords: string[];
  articulos_relacionados: string[];
  aplica_a: string[];
  referencias_legales: string[];
  vigencia: {
    estado: string;
    ultima_revision: string;
    nota: string;
  };
  fuente_oficial: {
    tipo: string;
    referencia: string;
    url: string;
  };
};

export type SearchableDoc = {
  id: string;
  titulo: string;
  texto_simple: string;
  keywords: string[];
  codigo_infraccion: string | null;
  coleccion: string;
  slug: string;
};

export type SearchResultItem = SearchableDoc & {
  score: number;
};

export type SearchResponse = {
  results: SearchResultItem[];
  explanation: string | null;
  keywords: string[];
  source: "fuse-direct" | "gemini-enhanced";
};

export const COLLECTIONS = [
  "abusos",
  "alcoholemia",
  "definiciones",
  "derechos",
  "disposiciones-finales",
  "infracciones-131",
  "leyes-complementarias",
  "normas-comportamiento",
  "normas-sanciones",
  "procedimientos",
] as const;

export type CollectionName = (typeof COLLECTIONS)[number];
