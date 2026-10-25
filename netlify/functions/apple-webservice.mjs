import { buildPass } from '../../lib/apple.mjs';
import { config as app } from '../../lib/config.mjs';
import { appleRegister, appleUnregister, appleUpdatedSerials, getClientBySerial } from '../../lib/db.mjs';
import { handle, json, readJson, UUID } from '../../lib/http.mjs';

/**
 * Apple Wallet web service (developer.apple.com/documentation/walletpasses/adding-a-web-service-to-update-passes).
 * Чрез него iPhone-ът се записва за обновления и тегли новата версия на картата след всеки печат.
 */
export default handle(async (req) => {
  const parts = new URL(req.url).pathname.replace(/^.*\/api\/apple\/v1\//, '').split('/');

  // POST /v1/log
  if (parts[0] === 'log') {
    console.log('Apple Wallet log', JSON.stringify(await readJson(req)));
    return new Response(null, { status: 200 });
  }

  // /v1/devices/:device/registrations/:passType[/:serial]
  if (parts[0] === 'devices' && parts[2] === 'registrations') {
    const [, deviceLibraryId, , passTypeId, serial] = parts;
    if (passTypeId !== app.apple.passTypeId) return new Response(null, { status: 404 });

    if (serial === undefined && req.method === 'GET') {
      const since = new URL(req.url).searchParams.get('passesUpdatedSince');
      const rows = await appleUpdatedSerials({ deviceLibraryId, passTypeId, since });
      if (!rows.length) return new Response(null, { status: 204 });
      const lastUpdated = Math.max(...rows.map((r) => new Date(r.updated_at).getTime()));
      return json({ serialNumbers: rows.map((r) => r.serial), lastUpdated: String(lastUpdated) });
    }

    const client = await authorized(req, serial);
    if (!client) return new Response(null, { status: 401 });

    if (req.method === 'POST') {
      const pushToken = (await readJson(req))?.pushToken;
      if (!pushToken) return new Response(null, { status: 400 });
      const status = await appleRegister({ deviceLibraryId, passTypeId, serial: client.serial, pushToken });
      return new Response(null, { status: status === 'created' ? 201 : 200 });
    }
    if (req.method === 'DELETE') {
      await appleUnregister({ deviceLibraryId, passTypeId, serial: client.serial });
      return new Response(null, { status: 200 });
    }
  }

  // GET /v1/passes/:passType/:serial
  if (parts[0] === 'passes' && req.method === 'GET') {
    const [, passTypeId, serial] = parts;
    if (passTypeId !== app.apple.passTypeId) return new Response(null, { status: 404 });
    const client = await authorized(req, serial);
    if (!client) return new Response(null, { status: 401 });

    const modified = new Date(client.updated_at);
    modified.setMilliseconds(0);
    const since = req.headers.get('if-modified-since');
    if (since && new Date(since) >= modified) return new Response(null, { status: 304 });
    return new Response(await buildPass(client), {
      headers: { 'content-type': 'application/vnd.apple.pkpass', 'last-modified': modified.toUTCString() },
    });
  }

  return new Response(null, { status: 404 });
});

async function authorized(req, serial) {
  if (!UUID.test(serial ?? '')) return null;
  const token = (req.headers.get('authorization') ?? '').replace(/^ApplePass\s+/i, '');
  const client = await getClientBySerial(serial.toLowerCase());
  return client && token && client.auth_token === token ? client : null;
}

export const config = { path: '/api/apple/v1/*' };
