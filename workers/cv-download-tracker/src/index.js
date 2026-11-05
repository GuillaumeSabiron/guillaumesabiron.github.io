const CVS = {
  fr: "https://guillaumesabiron.github.io/static/documents/guillaume-sabiron-cv-fr.pdf",
  en: "https://guillaumesabiron.github.io/static/documents/guillaume-sabiron-cv-en.pdf",
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const language = url.pathname.replace(/^\//, "").replace(/\/$/, "");

    if (!Object.hasOwn(CVS, language)) {
      return new Response("Not found", { status: 404 });
    }

    if (!["GET", "HEAD"].includes(request.method)) {
      return new Response("Method not allowed", {
        status: 405,
        headers: { Allow: "GET, HEAD", "Cache-Control": "no-store" },
      });
    }

    // Intentionally record only the requested CV variant and the timestamp
    // automatically attached by Analytics Engine. No IP address, referrer,
    // user agent, or other visitor identifier is stored here.
    // A redirect request is NOT proof of a completed download or a unique
    // visitor. HEAD checks and browser prefetches must not inflate this metric.
    const purpose = `${request.headers.get("Purpose") || ""} ${request.headers.get("Sec-Purpose") || ""}`;
    if (request.method === "GET" && !/prefetch|prerender/i.test(purpose)) {
      try {
        env.CV_DOWNLOADS.writeDataPoint({
          blobs: [language, "cv_request"],
          doubles: [1],
          indexes: ["cv-download"],
        });
      } catch {
        // Measurement must never prevent access to the CV. Do not log visitor
        // details when the binding is missing or unavailable.
        console.warn("CV request measurement unavailable");
      }
    }

    return new Response(null, {
      status: 302,
      headers: { Location: CVS[language], "Cache-Control": "no-store" },
    });
  },
};
