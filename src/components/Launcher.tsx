import { useState, useRef } from "react";
import type { ArticleResult } from "@/lib/types";
import { formatSancion } from "@/lib/sancion";

export default function Launcher() {
  const [query, setQuery] = useState("");
  const [candidates, setCandidates] = useState<ArticleResult[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSearch = async (q: string) => {
    const trimmed = q.trim();
    if (trimmed.length < 2) return;

    setLoading(true);
    setError(null);
    setCandidates(null);

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);

    try {
      const res = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: trimmed }),
        signal: controller.signal,
      });
      clearTimeout(timeout);
      const data = await res.json() as { candidates: ArticleResult[] };

      if (data.candidates && data.candidates.length > 0) {
        setCandidates(data.candidates);
      }
    } catch (e) {
      if (e instanceof DOMException && e.name === "AbortError") {
        setError("La búsqueda está tardando más de lo normal. Intenta de nuevo.");
      } else {
        setError("Ocurrió un error. Verifica que el servidor esté funcionando.");
      }
    } finally {
      clearTimeout(timeout);
      setLoading(false);
    }
  };

  const onSubmit = (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleSearch(query);
  };

  const onReset = () => {
    setQuery("");
    setCandidates(null);
    setError(null);
    setLoading(false);
    inputRef.current?.focus();
  };

  return (
    <div>
      <form onSubmit={onSubmit} style={{ display: "flex", gap: "0.5rem" }}>
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Describe tu situación (ej. un tombo me pedía plata pa no multarme)..."
          aria-label="Describe tu situación de tránsito"
          style={{
            flex: 1,
            padding: "0.75rem 1rem",
            fontSize: "1.125rem",
            border: "2px solid #ccc",
            borderRadius: "8px",
            boxSizing: "border-box",
          }}
        />
        <button
          type="submit"
          disabled={loading || query.trim().length < 2 || undefined}
          suppressHydrationWarning
          style={{
            padding: "0.75rem 1.25rem",
            fontSize: "1.125rem",
            background: loading ? "#ccc" : "#1a5fb4",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            cursor: loading ? "default" : "pointer",
          }}
        >
          Buscar
        </button>
      </form>

      {loading && (
        <p style={{ marginTop: "1rem", color: "#666" }}>
          Buscando artículos relacionados...
        </p>
      )}

      {error && !loading && (
        <p style={{ marginTop: "1rem", color: "#c33", background: "#fee", padding: "0.75rem", borderRadius: "8px" }}>
          {error}
          <br />
          <button onClick={onReset} style={{ background: "none", border: "none", color: "#1a5fb4", cursor: "pointer", textDecoration: "underline", marginTop: "0.5rem", padding: 0 }}>
            Intentar de nuevo
          </button>
        </p>
      )}

      {candidates && !loading && (
        <div style={{ marginTop: "1rem" }}>
          {candidates.map((article) => (
            <article key={article.id} style={{ marginBottom: "1.5rem", paddingBottom: "1rem", borderBottom: "1px solid #eee" }}>
              <h2 style={{ marginBottom: "0.25rem", fontSize: "1.2rem" }}>
                <a href={article.slug} style={{ color: "#1a5fb4", textDecoration: "none" }}>
                  {article.titulo}
                </a>
              </h2>

              {article.codigo_infraccion && (
                <p style={{ margin: "0 0 0.25rem", fontSize: "0.85rem", color: "#555" }}>
                  <strong>Código de infracción:</strong> {article.codigo_infraccion}
                </p>
              )}
              {article.numero && (
                <p style={{ margin: "0 0 0.25rem", fontSize: "0.85rem", color: "#555" }}>
                  <strong>Artículo:</strong> {article.numero}
                </p>
              )}
              {!!formatSancion(article.sancion) && (
                <p style={{ margin: "0 0 0.5rem", fontSize: "0.85rem", color: "#555" }}>
                  <strong>Sanción:</strong> {formatSancion(article.sancion)}
                </p>
              )}

              <p style={{ margin: "0 0 0.5rem", lineHeight: 1.5 }}>{article.texto_simple}</p>

              {article.aplica_a && article.aplica_a.length > 0 && (
                <section style={{ marginTop: "0.5rem" }}>
                  <h3 style={{ fontSize: "0.85rem", marginBottom: "0.25rem", color: "#555" }}>Aplica a</h3>
                  <p style={{ margin: 0, fontSize: "0.85rem", color: "#666" }}>
                    {article.aplica_a.join(", ")}
                  </p>
                </section>
              )}

              {article.referencias_legales && article.referencias_legales.length > 0 && (
                <section style={{ marginTop: "0.25rem" }}>
                  <h3 style={{ fontSize: "0.85rem", marginBottom: "0.25rem", color: "#555" }}>Referencias legales</h3>
                  <ul style={{ margin: 0, fontSize: "0.85rem", color: "#666" }}>
                    {article.referencias_legales.map((ref, i) => <li key={i}>{ref}</li>)}
                  </ul>
                </section>
              )}

              <p style={{ marginTop: "0.5rem", fontSize: "0.85rem" }}>
                <a href={article.slug}>Ver artículo completo &rarr;</a>
              </p>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
