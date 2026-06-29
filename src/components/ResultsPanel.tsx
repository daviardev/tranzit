import type { SearchResultItem } from "@/lib/types";

type Props = {
  results: SearchResultItem[];
};

export default function ResultsPanel({ results }: Props) {
  if (!results || results.length === 0) return null;

  return (
    <div style={{ marginTop: "1rem" }}>
      <p style={{ fontSize: "0.85rem", color: "#666", marginBottom: "0.5rem" }}>
        {results.length} resultado{results.length !== 1 ? "s" : ""} encontrado{results.length !== 1 ? "s" : ""}
      </p>
      <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
        {results.map((item, i) => {
          const relevance = Math.round((1 - item.score) * 100);
          return (
            <li
              key={`${item.slug}-${i}`}
              style={{
                padding: "1rem",
                marginBottom: "0.5rem",
                border: "1px solid #ddd",
                borderRadius: "8px",
                background: "#fff",
              }}
            >
              <a href={item.slug} style={{ textDecoration: "none", color: "inherit" }}>
                <h3 style={{ margin: "0 0 0.25rem", fontSize: "1rem" }}>{item.titulo}</h3>
                {item.codigo_infraccion && (
                  <p style={{ margin: "0 0 0.25rem", fontSize: "0.85rem", color: "#555" }}>
                    <strong>Código:</strong> {item.codigo_infraccion}
                  </p>
                )}
                <span
                  style={{
                    display: "inline-block",
                    fontSize: "0.75rem",
                    padding: "0.125rem 0.5rem",
                    borderRadius: "999px",
                    background: relevance >= 80 ? "#e6f7e6" : "#fff3cd",
                    color: relevance >= 80 ? "#2d6a2d" : "#856404",
                  }}
                >
                  Relevancia: {relevance}%
                </span>
              </a>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
