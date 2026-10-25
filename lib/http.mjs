export const json = (body, status = 200, headers = {}) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...headers },
  });

export async function readJson(req) {
  try {
    return await req.json();
  } catch {
    return null;
  }
}

/** Обвивка, която връща 500 с лог вместо да показва детайли за грешката навън. */
export const handle = (fn) => async (req, context) => {
  try {
    return await fn(req, context);
  } catch (err) {
    console.error(err);
    return json({ error: 'server_error' }, 500);
  }
};

export const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
