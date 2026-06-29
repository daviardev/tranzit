import type { APIRoute } from "astro";

import { search } from "@/lib/search";

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = (await request.json()) as { query?: string };
    const query = body.query?.trim() ?? "";

    if (query.length < 2) {
      return new Response(
        JSON.stringify({
          results: [],
          explanation: null,
          keywords: [],
          source: "fuse-direct",
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      );
    }

    const result = await search(query);

    return new Response(JSON.stringify(result), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch {
    return new Response(
      JSON.stringify({
        results: [],
        explanation: null,
        keywords: [],
        source: "fuse-direct",
      }),
      { status: 200, headers: { "Content-Type": "application/json" } },
    );
  }
};
