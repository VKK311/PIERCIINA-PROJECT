import jwt from 'jsonwebtoken';
import { config, qrPayload } from './config.mjs';
import { readSecret } from './db.mjs';
import { isRewardReady, progressText } from './rules.mjs';

const API = 'https://walletobjects.googleapis.com/walletobjects/v1';

export const googleEnabled = () => Boolean(config.google.issuerId);

const classId = () => `${config.google.issuerId}.pierciina_loyalty`;
const objectId = (serial) => `${config.google.issuerId}.${serial.replace(/-/g, '')}`;

let serviceAccount;
async function account() {
  serviceAccount ??= JSON.parse((await readSecret('google-service-account.json')).toString('utf8'));
  return serviceAccount;
}

function loyaltyClass() {
  const { card, siteUrl } = config;
  return {
    id: classId(),
    issuerName: card.organization,
    programName: card.title,
    programLogo: { sourceUri: { uri: `${siteUrl}/api/img/logo.png` } },
    hexBackgroundColor: card.bg,
    reviewStatus: 'UNDER_REVIEW',
  };
}

export function loyaltyObject(client) {
  const { card, siteUrl, stampsForReward } = config;
  return {
    id: objectId(client.serial),
    classId: classId(),
    state: 'ACTIVE',
    hexBackgroundColor: card.bg,
    loyaltyPoints: { label: 'Stars', balance: { string: `${client.stamps}/${stampsForReward}` } },
    barcode: { type: 'QR_CODE', value: qrPayload(client.serial) },
    heroImage: { sourceUri: { uri: `${siteUrl}/api/img/strip-${client.stamps}.png` } },
    textModulesData: [
      { id: 'reward', header: isRewardReady(client.stamps) ? 'Reward unlocked' : 'Next reward', body: progressText(client.stamps) },
    ],
  };
}

/** Линк „Add to Google Wallet“ (класът и обектът се създават при първото запазване). */
export async function saveUrl(client) {
  const sa = await account();
  const token = jwt.sign(
    {
      iss: sa.client_email,
      aud: 'google',
      typ: 'savetowallet',
      origins: [config.siteUrl],
      payload: { loyaltyClasses: [loyaltyClass()], loyaltyObjects: [loyaltyObject(client)] },
    },
    sa.private_key,
    { algorithm: 'RS256' },
  );
  return `https://pay.google.com/gp/v/save/${token}`;
}

let accessToken = { value: null, expires: 0 };
async function authHeader() {
  if (Date.now() < accessToken.expires - 60_000) return `Bearer ${accessToken.value}`;
  const sa = await account();
  const now = Math.floor(Date.now() / 1000);
  const assertion = jwt.sign(
    {
      iss: sa.client_email,
      scope: 'https://www.googleapis.com/auth/wallet_object.issuer',
      aud: 'https://oauth2.googleapis.com/token',
      iat: now,
      exp: now + 3600,
    },
    sa.private_key,
    { algorithm: 'RS256' },
  );
  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion }),
  });
  if (!res.ok) throw new Error(`Google token: ${res.status} ${await res.text()}`);
  const body = await res.json();
  accessToken = { value: body.access_token, expires: Date.now() + body.expires_in * 1000 };
  return `Bearer ${accessToken.value}`;
}

/** Обновява картата в Google Wallet; при отключена награда изпраща и известие. */
export async function updateGoogleObject(client, { notifyReward = false } = {}) {
  if (!googleEnabled()) return;
  const id = encodeURIComponent(objectId(client.serial));
  const headers = { authorization: await authHeader(), 'content-type': 'application/json' };
  const { barcode, ...patch } = loyaltyObject(client);
  const res = await fetch(`${API}/loyaltyObject/${id}`, { method: 'PATCH', headers, body: JSON.stringify(patch) });
  if (res.status === 404) return; // клиентът не е добавил картата в Google Wallet
  if (!res.ok) throw new Error(`Google update: ${res.status} ${await res.text()}`);
  if (notifyReward) {
    await fetch(`${API}/loyaltyObject/${id}/addMessage`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        message: {
          id: `reward-${Date.now()}`,
          header: 'Pierciina',
          body: '50% OFF your next piercing ✦',
          messageType: 'TEXT_AND_NOTIFY',
        },
      }),
    });
  }
}
