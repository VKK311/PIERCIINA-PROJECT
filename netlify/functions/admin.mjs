import { login, verify } from '../../lib/auth.mjs';
import { parseQrPayload } from '../../lib/config.mjs';
import { listClients } from '../../lib/db.mjs';
import { handle, json, readJson, UUID } from '../../lib/http.mjs';
import { performAction, publicClient } from '../../lib/service.mjs';

/**
 * POST /api/admin/login   {email, password}  → {token}
 * POST /api/admin/scan    {code}             → сканиране: добавя 1 печат автоматично
 * POST /api/admin/action  {serial, action}   → stamp | remove | redeem
 * GET  /api/admin/clients ?q=                → списък с клиенти
 */
export default handle(async (req) => {
  const route = new URL(req.url).pathname.split('/').pop();

  if (route === 'login' && req.method === 'POST') {
    const body = await readJson(req);
    const token = login(body?.email, body?.password);
    return token ? json({ token }) : json({ error: 'invalid_credentials' }, 401);
  }

  if (!verify(req)) return json({ error: 'unauthorized' }, 401);

  if (route === 'clients' && req.method === 'GET') {
    const rows = await listClients(new URL(req.url).searchParams.get('q'));
    return json({ clients: rows.map(publicClient) });
  }

  if (route === 'scan' && req.method === 'POST') {
    const serial = parseQrPayload((await readJson(req))?.code);
    if (!serial) return json({ error: 'unknown_code' }, 400);
    return respond(await performAction(serial, 'stamp'));
  }

  if (route === 'action' && req.method === 'POST') {
    const body = await readJson(req);
    const serial = String(body?.serial ?? '').toLowerCase();
    if (!UUID.test(serial) || !['stamp', 'remove', 'redeem'].includes(body?.action)) return json({ error: 'invalid' }, 400);
    return respond(await performAction(serial, body.action));
  }

  return json({ error: 'not_found' }, 404);
});

function respond({ error, client, result }) {
  if (error === 'not_found') return json({ error }, 404);
  if (error) return json({ error }, 409);
  return json({ result, client: publicClient(client) });
}

export const config = { path: '/api/admin/*' };
