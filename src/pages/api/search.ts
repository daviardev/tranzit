import type { APIRoute } from "astro";

import { search } from "@/lib/search";

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = (await request.json()) as { query?: string };
    const query = body.query?.trim() ?? "";

    const candidates = await search(query);

    return new Response(JSON.stringify({ candidates }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch {
    return new Response(
      JSON.stringify({ candidates: [] }),
      { status: 200, headers: { "Content-Type": "application/json" } },
    );
  }
};
