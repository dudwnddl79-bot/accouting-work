export default async (request, context) => {
  const PASSWORD = Deno.env.get("SITE_PASSWORD") || "";
  const USER = Deno.env.get("SITE_USER") || "admin";

  const authHeader = request.headers.get("authorization");
  if (authHeader && authHeader.startsWith("Basic ")) {
    try {
      const decoded = atob(authHeader.slice(6));
      const colonIdx = decoded.indexOf(":");
      const u = decoded.slice(0, colonIdx);
      const p = decoded.slice(colonIdx + 1);
      if (u === USER && p === PASSWORD && PASSWORD !== "") {
        return context.next();
      }
    } catch (_) {}
  }

  return new Response("접근하려면 로그인이 필요합니다.", {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="업무 포털", charset="UTF-8"',
      "Content-Type": "text/plain; charset=utf-8",
    },
  });
};
