import http2 from 'node:http2';
import { PKPass } from 'passkit-generator';
import { config, qrPayload } from './config.mjs';
import { applePushTokens, appleUnregisterToken, readSecret } from './db.mjs';
import { applePassImages } from './images.mjs';
import { isRewardReady, progressText } from './rules.mjs';

const rgb = (hex) => {
  const n = parseInt(hex.replace('#', ''), 16);
  return `rgb(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255})`;
};

/**
 * Полетата на картата. Наградата е отделно поле с changeMessage и съществува само докато е
 * отключена — така iPhone показва известие единствено при отключване, а не при всеки печат.
 */
export function passFields(client) {
  const total = config.stampsForReward;
  const fields = {
    headerFields: [{ key: 'stars', label: 'STARS', value: `${client.stamps}/${total}` }],
    secondaryFields: [],
  };
  if (isRewardReady(client.stamps)) {
    fields.secondaryFields.push({
      key: 'reward',
      label: 'REWARD UNLOCKED',
      value: progressText(client.stamps),
      changeMessage: 'Pierciina: %@',
    });
  } else {
    fields.secondaryFields.push({ key: 'progress', label: 'NEXT REWARD', value: progressText(client.stamps) });
  }
  return fields;
}

async function certificates() {
  const [wwdr, signerCert, signerKey] = await Promise.all([
    readSecret('wwdr.pem'),
    readSecret('signerCert.pem'),
    readSecret('signerKey.pem'),
  ]);
  return { wwdr, signerCert, signerKey, signerKeyPassphrase: config.apple.keyPassphrase };
}

export async function buildPass(client) {
  const { card, studio, apple, siteUrl } = config;
  const pass = new PKPass(await applePassImages(client.stamps), await certificates(), {
    formatVersion: 1,
    passTypeIdentifier: apple.passTypeId,
    teamIdentifier: apple.teamId,
    serialNumber: client.serial,
    organizationName: card.organization,
    description: card.title,
    logoText: card.title,
    foregroundColor: rgb(card.fg),
    backgroundColor: rgb(card.bg),
    labelColor: rgb(card.label),
    webServiceURL: `${siteUrl}/api/apple`,
    authenticationToken: client.auth_token,
    sharingProhibited: true,
  });
  pass.type = 'storeCard';
  pass.setLocations({ latitude: studio.lat, longitude: studio.lng, relevantText: 'Pierciina is around the corner ✦' });
  const fields = passFields(client);
  pass.headerFields.push(...fields.headerFields);
  pass.secondaryFields.push(...fields.secondaryFields);
  pass.setBarcodes({ message: qrPayload(client.serial), format: 'PKBarcodeFormatQR', messageEncoding: 'iso-8859-1' });
  return pass.getAsBuffer();
}

/** Казва на всички iPhone-и с тази карта да изтеглят новата версия (APNs, празен payload). */
export async function pushPassUpdate(serial) {
  const tokens = await applePushTokens(serial);
  if (!tokens.length) return;
  const { signerCert, signerKey, signerKeyPassphrase } = await certificates();
  const session = http2.connect('https://api.push.apple.com', {
    cert: signerCert,
    key: signerKey,
    passphrase: signerKeyPassphrase,
  });
  session.on('error', (err) => console.error('APNs session error', err));
  try {
    await Promise.all(
      tokens.map(
        (token) =>
          new Promise((resolve) => {
            const req = session.request({
              ':method': 'POST',
              ':path': `/3/device/${token}`,
              'apns-topic': config.apple.passTypeId,
              'content-type': 'application/json',
            });
            let status = 0;
            req.on('response', (headers) => (status = headers[':status']));
            req.on('error', (err) => {
              console.error('APNs push failed', err);
              resolve();
            });
            req.on('close', async () => {
              // 410 = картата е изтрита от устройството.
              if (status === 410) await appleUnregisterToken(token).catch(() => {});
              else if (status !== 200) console.error('APNs status', status);
              resolve();
            });
            req.end('{}');
          }),
      ),
    );
  } finally {
    session.close();
  }
}
