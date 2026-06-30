import type { SancionValue } from "./sancion";

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
  sancion: SancionValue;
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

export type ArticleResult = {
  id: string;
  titulo: string;
  texto_simple: string;
  codigo_infraccion: string | null;
  sancion: SancionValue;
  numero: string | null;
  aplica_a: string[];
  referencias_legales: string[];
  articulos_relacionados: string[];
  vigencia: LawEntry["vigencia"] | null;
  fuente_oficial: LawEntry["fuente_oficial"] | null;
  slug: string;
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
