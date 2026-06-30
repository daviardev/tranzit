export type SancionValue =
  | { valor_smdlv?: number; inmovilizacion?: boolean }
  | string
  | null
  | undefined;

export function formatSancion(s: unknown): string | null {
  if (s == null) return null;
  if (typeof s === "string") {
    if (s === "MISSING") return null;
    return s;
  }
  if (typeof s === "object") {
    const obj = s as Record<string, unknown>;
    const parts: string[] = [];
    if (typeof obj.valor_smdlv === "number") {
      parts.push(`${obj.valor_smdlv} SMLDV`);
    }
    if (obj.inmovilizacion === true) {
      parts.push("Inmovilización");
    }
    return parts.length > 0 ? parts.join(" + ") : null;
  }
  return null;
}
