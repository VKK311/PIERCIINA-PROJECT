import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { before, test } from 'node:test';

// Тестов (самоподписан) сертификат вместо истинския от Apple — проверяваме съдържанието на картата.
const dir = mkdtempSync(join(tmpdir(), 'pierciina-pass-'));
const openssl = (...args) => execFileSync('openssl', args, { stdio: 'ignore' });

let apple, images, google;
before(async () => {
  openssl('req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-days', '1', '-subj', '/CN=test',
    '-keyout', join(dir, 'signerKey.pem'), '-out', join(dir, 'signerCert.pem'));
  openssl('req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-days', '1', '-subj', '/CN=wwdr',
    '-keyout', join(dir, 'wwdr-key.pem'), '-out', join(dir, 'wwdr.pem'));
  Object.assign(process.env, {
    LOCAL_SECRETS_DIR: dir,
    APPLE_TEAM_ID: 'TEAM123456',
    SITE_URL: 'https://card.example.com',
    GOOGLE_ISSUER_ID: '3388000000000000000',
  });
  apple = await import('../lib/apple.mjs');
  images = await import('../lib/images.mjs');
  google = await import('../lib/google.mjs');
});

const client = (stamps) => ({
  serial: '3f2a9c1e-5b7d-4e8a-9c21-7d4e5f6a8b90',
  auth_token: 'a'.repeat(64),
  stamps,
});

function unpack(buffer) {
  const file = join(dir, `pass-${Date.now()}.pkpass`);
  writeFileSync(file, buffer);
  const list = execFileSync('unzip', ['-Z1', file]).toString().trim().split('\n').sort();
  const pass = JSON.parse(execFileSync('unzip', ['-p', file, 'pass.json']).toString());
  return { list, pass };
}

test('картата за Apple Wallet съдържа печатите, баркода и web service', async () => {
  const { list, pass } = unpack(await apple.buildPass(client(3)));

  for (const name of ['pass.json', 'manifest.json', 'signature', 'icon.png', 'icon@2x.png', 'logo.png', 'strip.png', 'strip@2x.png']) {
    assert.ok(list.includes(name), `missing ${name}`);
  }
  assert.equal(pass.serialNumber, client(3).serial);
  assert.equal(pass.passTypeIdentifier, 'pass.com.pierciina.loyalty');
  assert.equal(pass.teamIdentifier, 'TEAM123456');
  assert.equal(pass.logoText, 'Pierciina Loyalty Card');
  assert.equal(pass.webServiceURL, 'https://card.example.com/api/apple');
  assert.equal(pass.authenticationToken, 'a'.repeat(64));
  assert.equal(pass.storeCard.headerFields[0].value, '3/5');
  assert.equal(pass.storeCard.secondaryFields[0].key, 'progress');
  assert.equal(pass.storeCard.backFields?.length ?? 0, 0);
  assert.equal(pass.barcodes[0].message, `PIERCIINA:${client(3).serial}`);
  assert.equal(pass.barcodes[0].format, 'PKBarcodeFormatQR');
  assert.ok(pass.locations[0].latitude > 42 && pass.locations[0].latitude < 43);
});

test('известие на iPhone само при отключена награда', () => {
  for (let s = 0; s < 5; s++) {
    const fields = apple.passFields(client(s));
    assert.ok(fields.headerFields.concat(fields.secondaryFields).every((f) => !f.changeMessage), `stamps=${s}`);
  }
  const unlocked = apple.passFields(client(5)).secondaryFields[0];
  assert.equal(unlocked.key, 'reward');
  assert.match(unlocked.changeMessage, /%@/);
});

test('изображенията се генерират в точните размери', async () => {
  const sharp = (await import('sharp')).default;
  const files = await images.applePassImages(2);
  const size = async (name) => {
    const { width, height } = await sharp(files[name]).metadata();
    return [width, height];
  };
  assert.deepEqual(await size('strip@2x.png'), [750, 246]);
  assert.deepEqual(await size('icon@2x.png'), [58, 58]);
  assert.equal((await images.stripSvg(2)).match(/<path/g).length, 5);
  assert.ok(await images.publicImage('strip-5.png'));
  assert.equal(await images.publicImage('strip-9.png'), null);
});

test('обект за Google Wallet', () => {
  const obj = google.loyaltyObject(client(4));
  assert.equal(obj.id, '3388000000000000000.3f2a9c1e5b7d4e8a9c217d4e5f6a8b90');
  assert.equal(obj.loyaltyPoints.balance.string, '4/5');
  assert.equal(obj.heroImage.sourceUri.uri, 'https://card.example.com/api/img/strip-4.png');
  assert.equal(obj.barcode.value, `PIERCIINA:${client(4).serial}`);
});
