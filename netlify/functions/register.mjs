import { createClientCard } from '../../lib/db.mjs';
import { handle, json, readJson } from '../../lib/http.mjs';
import { clientLines, emailAdmin } from '../../lib/notify.mjs';
import { validateRegistration } from '../../lib/rules.mjs';

export default handle(async (req) => {
  if (req.method !== 'POST') return json({ error: 'method_not_allowed' }, 405);
  const body = await readJson(req);
  // Скрито поле срещу ботове: хората не го виждат и не го попълват.
  if (body?.website) return json({ error: 'invalid' }, 400);
  const { ok, errors, value } = validateRegistration(body);
  if (!ok) return json({ error: 'invalid', fields: errors }, 400);

  const client = await createClientCard(value);
  await emailAdmin(`Pierciina: нова карта — ${client.name}`, clientLines(client)).catch(console.error);
  return json({ serial: client.serial }, 201);
});

export const config = { path: '/api/register' };
