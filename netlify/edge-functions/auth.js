const getEnv = (k, d = "") => { try { return Deno.env.get(k) || d; } catch (_) { return d; } };

export default async (request, context) => {
  const PASSWORD = getEnv("SITE_PASSWORD");
  const USER = getEnv("SITE_USER", "admin");

  // 비밀번호 미설정 시 그냥 통과
  if (!PASSWORD) return context.next();

  const authHeader = request.headers.get("authorization") || "";
  if (authHeader.startsWith("Basic ")) {
    try {
      const decoded = atob(authHeader.slice(6));
      const sep = decoded.indexOf(":");
      if (sep > -1) {
        const u = decoded.slice(0, sep);
        const p = decoded.slice(sep + 1);
        if (u === USER && p === PASSWORD) return context.next();
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
