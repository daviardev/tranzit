import { useState, useCallback, useRef, useEffect } from "react";
import ResultsPanel from "@/components/ResultsPanel";
import type { SearchResponse, SearchResultItem } from "@/lib/types";

export default function Launcher() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [explanation, setExplanation] = useState<string | null>(null);
  const [keywords, setKeywords] = useState<string[]>([]);
  const [source, setSource] = useState<SearchResponse["source"]>("fuse-direct");
  const [loading, setLoading] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const handleSearch = useCallback(async (q: string) => {
    if (q.length < 2) {
      setResults([]);
      setExplanation(null);
      setKeywords([]);
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q }),
      });
      const data = (await res.json()) as SearchResponse;
      setResults(data.results ?? []);
      setExplanation(data.explanation ?? null);
      setKeywords(data.keywords ?? []);
      setSource(data.source ?? "fuse-direct");
    } catch {
      setResults([]);
      setExplanation(null);
      setKeywords([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setQuery(val);
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => handleSearch(val), 300);
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      if (timerRef.current) clearTimeout(timerRef.current);
      handleSearch(query);
    }
  };

  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  const showGeminiBlock = source === "gemini-enhanced" && explanation;

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={onChange}
        onKeyDown={onKeyDown}
        placeholder="Describe tu situación (ej. me pararon sin casco en la moto)..."
        aria-label="Buscar en el Código Nacional de Tránsito"
        style={{
          width: "100%",
          padding: "0.75rem 1rem",
          fontSize: "1.125rem",
          border: "2px solid #ccc",
          borderRadius: "8px",
        }}
      />

      {loading && (
        <p style={{ marginTop: "0.5rem", color: "#666" }}>Buscando...</p>
      )}

      {showGeminiBlock && (
        <div
          style={{
            marginTop: "1rem",
            padding: "1rem",
            background: "#f0f7ff",
            borderRadius: "8px",
            borderLeft: "4px solid #1a5fb4",
          }}
        >
          <p style={{ margin: 0, whiteSpace: "pre-wrap" }}>{explanation}</p>
          {keywords.length > 0 && (
            <p
              style={{
                marginTop: "0.5rem",
                fontSize: "0.85rem",
                color: "#666",
              }}
            >
              Términos buscados: {keywords.join(", ")}
            </p>
          )}
        </div>
      )}

      <ResultsPanel results={results} />

      {!loading &&
        query.length >= 2 &&
        results.length === 0 &&
        !explanation && (
          <p style={{ marginTop: "1rem", color: "#999" }}>
            No se encontraron artículos. Intenta con otras palabras.
          </p>
        )}
    </div>
  );
}
