import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { createClient } from '@supabase/supabase-js';
import { config } from './config.mjs';

let client;
export function supabase() {
  if (!client) {
    if (!config.supabase.url || !config.supabase.serviceKey) {
      throw new Error('SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY are not set');
    }
    client = createClient(config.supabase.url, config.supabase.serviceKey, {
      auth: { persistSession: false },
    });
  }
  return client;
}

const must = ({ data, error }) => {
  if (error) throw new Error(error.message);
  return data;
};

const CLIENT_COLUMNS = 'id, serial, auth_token, name, email, phone, stamps, rewards_redeemed, active, created_at, updated_at';

/** Нова карта. Предишна активна карта със същия телефон се архивира (една карта на телефон). */
export async function createClientCard({ name, email, phone }) {
  must(await supabase().from('clients').update({ active: false }).eq('phone', phone).eq('active', true));
  return must(await supabase().from('clients').insert({ name, email, phone }).select(CLIENT_COLUMNS).single());
}

export async function getClientBySerial(serial) {
  return must(await supabase().from('clients').select(CLIENT_COLUMNS).eq('serial', serial).maybeSingle());
}

export async function listClients(query) {
  let q = supabase().from('clients').select(CLIENT_COLUMNS).eq('active', true).order('updated_at', { ascending: false }).limit(500);
  const term = String(query ?? '').trim().replace(/[%,()]/g, '');
  if (term) q = q.or(`name.ilike.%${term}%,phone.ilike.%${term}%,email.ilike.%${term}%`);
  return must(await q);
}

/**
 * Записва новия брой печати само ако никой не го е променил междувременно
 * (две бързи сканирания на същата карта не дават двоен печат).
 */
export async function updateStamps(client, nextStamps, action) {
  const patch = { stamps: nextStamps, updated_at: new Date().toISOString() };
  if (action === 'redeem') patch.rewards_redeemed = client.rewards_redeemed + 1;
  const rows = must(
    await supabase().from('clients').update(patch).eq('id', client.id).eq('stamps', client.stamps).select(CLIENT_COLUMNS),
  );
  if (!rows.length) return null;
  must(await supabase().from('stamp_events').insert({ client_id: client.id, action, stamps_after: nextStamps }));
  return rows[0];
}

export async function appleRegister({ deviceLibraryId, passTypeId, serial, pushToken }) {
  const existing = must(
    await supabase()
      .from('apple_registrations')
      .select('push_token')
      .match({ device_library_id: deviceLibraryId, pass_type_id: passTypeId, serial })
      .maybeSingle(),
  );
  must(
    await supabase()
      .from('apple_registrations')
      .upsert({ device_library_id: deviceLibraryId, pass_type_id: passTypeId, serial, push_token: pushToken }),
  );
  return existing ? 'updated' : 'created';
}

export async function appleUnregister({ deviceLibraryId, passTypeId, serial }) {
  must(
    await supabase()
      .from('apple_registrations')
      .delete()
      .match({ device_library_id: deviceLibraryId, pass_type_id: passTypeId, serial }),
  );
}

export async function appleUnregisterToken(pushToken) {
  must(await supabase().from('apple_registrations').delete().eq('push_token', pushToken));
}

export async function applePushTokens(serial) {
  const rows = must(await supabase().from('apple_registrations').select('push_token').eq('serial', serial));
  return [...new Set(rows.map((r) => r.push_token))];
}

export async function appleUpdatedSerials({ deviceLibraryId, passTypeId, since }) {
  const regs = must(
    await supabase()
      .from('apple_registrations')
      .select('serial')
      .match({ device_library_id: deviceLibraryId, pass_type_id: passTypeId }),
  );
  if (!regs.length) return [];
  let q = supabase().from('clients').select('serial, updated_at').in('serial', regs.map((r) => r.serial));
  if (since) q = q.gt('updated_at', new Date(Number(since)).toISOString());
  return must(await q);
}

/** Файлове от частния bucket (сертификати), кеширани в паметта на функцията. */
const secretCache = new Map();
export async function readSecret(name) {
  if (!secretCache.has(name) && config.supabase.secretsDir) {
    // Локална разработка и тестове: файловете са в папка вместо в Supabase Storage.
    secretCache.set(name, readFileSync(join(config.supabase.secretsDir, name)));
  }
  if (!secretCache.has(name)) {
    const { data, error } = await supabase().storage.from(config.supabase.secretsBucket).download(name);
    if (error) throw new Error(`Secret ${name}: ${error.message}`);
    secretCache.set(name, Buffer.from(await data.arrayBuffer()));
  }
  return secretCache.get(name);
}
