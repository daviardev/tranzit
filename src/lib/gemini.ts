import { GoogleGenerativeAI } from "@google/generative-ai";

import { getCached, setCache } from "@/lib/cache";

export type GeminiResponse = {
  keywords: string[];
  explanation: string | null;
};

const genAI = new GoogleGenerativeAI(import.meta.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

export async function interpretQuery(query: string): Promise<GeminiResponse> {
  const cacheKey = `gemini:${query.toLowerCase().trim()}`;
  const cached = getCached(cacheKey);
  if (cached) {
    return JSON.parse(cached) as GeminiResponse;
  }

  const prompt = `Eres un asistente de tránsito colombiano experto en la Ley 769 de 2002.

Un usuario preguntó: "${query}"

Haz dos cosas:
1. Extrae 3-8 palabras clave para buscar artículos en una base de datos de leyes de tránsito.
2. Prepara una explicación clara en lenguaje ciudadano (2-3 párrafos) que responda la consulta del usuario basada en la ley.

Responde SOLO con este JSON exacto, sin texto adicional, sin markdown:
{"keywords": ["palabra1", "palabra2"], "explanation": "explicación aquí"}`;

  const result = await model.generateContent(prompt);
  const text = result.response.text();

  const cleaned = text.replace(/```json?|```/g, "").trim();

  try {
    const parsed = JSON.parse(cleaned) as GeminiResponse;
    const response: GeminiResponse = {
      keywords: Array.isArray(parsed.keywords)
        ? parsed.keywords.slice(0, 8)
        : [],
      explanation:
        typeof parsed.explanation === "string" ? parsed.explanation : null,
    };
    setCache(cacheKey, JSON.stringify(response));
    return response;
  } catch {
    const response: GeminiResponse = { keywords: [], explanation: null };
    setCache(cacheKey, JSON.stringify(response));
    return response;
  }
}
