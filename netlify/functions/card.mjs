import { buildPass } from '../../lib/apple.mjs';
import { config as app } from '../../lib/config.mjs';
import { getClientBySerial } from '../../lib/db.mjs';
import { googleEnabled, saveUrl } from '../../lib/google.mjs';
import { handle, json, UUID } from '../../lib/http.mjs';
import { isRewardReady } from '../../lib/rules.mjs';

/**
 * GET /api/card/:serial        → данни за страницата след регистрация
 * GET /api/card/:serial.pkpass → картата за Apple Wallet
 */
export default handle(async (req, context) => {
  const raw = context.params.serial ?? '';
  const wantsPass = raw.endsWith('.pkpass');
  const serial = raw.replace(/\.pkpass$/, '').toLowerCase();
  if (!UUID.test(serial)) return json({ error: 'not_found' }, 404);
  const client = await getClientBySerial(serial);
  if (!client?.active) return json({ error: 'not_found' }, 404);

  if (wantsPass) {
    return new Response(await buildPass(client), {
      headers: {
        'content-type': 'application/vnd.apple.pkpass',
        'content-disposition': 'attachment; filename="pierciina.pkpass"',
        'last-modified': new Date(client.updated_at).toUTCString(),
        'cache-control': 'no-store',
      },
    });
  }

  return json({
    title: app.card.title,
    name: client.name,
    stamps: client.stamps,
    total: app.stampsForReward,
    rewardReady: isRewardReady(client.stamps),
    appleUrl: `/api/card/${client.serial}.pkpass`,
    googleUrl: googleEnabled() ? await saveUrl(client) : null,
  });
});

export const config = { path: '/api/card/:serial' };
