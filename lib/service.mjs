import { pushPassUpdate } from './apple.mjs';
import { getClientBySerial, updateStamps } from './db.mjs';
import { updateGoogleObject } from './google.mjs';
import { clientLines, emailAdmin } from './notify.mjs';
import { applyAction } from './rules.mjs';

/** Изпълнява действие на админа върху карта и обновява картата в портфейла на клиента. */
export async function performAction(serial, action) {
  for (let attempt = 0; attempt < 3; attempt++) {
    const client = await getClientBySerial(serial);
    if (!client || !client.active) return { error: 'not_found' };
    const outcome = applyAction(client.stamps, action);
    if (!outcome.changed) return { client, result: outcome.result };
    const updated = await updateStamps(client, outcome.stamps, action);
    if (!updated) continue; // друго сканиране е променило картата междувременно — опитай пак
    await propagate(updated, outcome.result);
    return { client: updated, result: outcome.result };
  }
  return { error: 'conflict' };
}

async function propagate(client, result) {
  const unlocked = result === 'reward_unlocked';
  const tasks = [pushPassUpdate(client.serial), updateGoogleObject(client, { notifyReward: unlocked })];
  if (unlocked) {
    tasks.push(emailAdmin(`Pierciina: ${client.name} отключи 50% отстъпка`, [...clientLines(client), 'Картата има 5 печата.']));
  }
  // Неуспешно известие не трябва да проваля печата — само го записваме в логовете.
  for (const r of await Promise.allSettled(tasks)) if (r.status === 'rejected') console.error(r.reason);
}

export const publicClient = (c) => ({
  serial: c.serial,
  name: c.name,
  phone: c.phone,
  email: c.email,
  stamps: c.stamps,
  rewardsRedeemed: c.rewards_redeemed,
  createdAt: c.created_at,
  updatedAt: c.updated_at,
});
