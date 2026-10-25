import assert from 'node:assert/strict';
import { test } from 'node:test';
import { parseQrPayload, qrPayload } from '../lib/config.mjs';
import { applyAction, normalizePhone, progressText, validateRegistration } from '../lib/rules.mjs';

test('5 сканирания отключват наградата, шестото не добавя', () => {
  let stamps = 0;
  const results = [];
  for (let i = 0; i < 6; i++) {
    const r = applyAction(stamps, 'stamp');
    stamps = r.stamps;
    results.push(r.result);
  }
  assert.deepEqual(results, ['stamped', 'stamped', 'stamped', 'stamped', 'reward_unlocked', 'reward_ready']);
  assert.equal(stamps, 5);
});

test('използването на наградата нулира картата', () => {
  assert.deepEqual(applyAction(5, 'redeem'), { stamps: 0, changed: true, result: 'redeemed' });
  assert.equal(applyAction(3, 'redeem').changed, false);
});

test('премахване на грешен печат', () => {
  assert.deepEqual(applyAction(2, 'remove'), { stamps: 1, changed: true, result: 'removed' });
  assert.equal(applyAction(0, 'remove').changed, false);
});

test('текст на напредъка', () => {
  assert.equal(progressText(0), '5 more stars to 50% off');
  assert.equal(progressText(4), '1 more star to 50% off');
  assert.equal(progressText(5), '50% OFF your next piercing');
});

test('телефони', () => {
  assert.equal(normalizePhone('0888 123 456'), '+359888123456');
  assert.equal(normalizePhone('+359 88 812 3456'), '+359888123456');
  assert.equal(normalizePhone('00447700900123'), '+447700900123');
  assert.equal(normalizePhone('123'), null);
});

test('валидиране на регистрацията', () => {
  const ok = validateRegistration({ name: '  Ина  Петрова ', email: 'Ina@Example.com', phone: '0888123456', consent: true });
  assert.equal(ok.ok, true);
  assert.deepEqual(ok.value, { name: 'Ина Петрова', email: 'ina@example.com', phone: '+359888123456' });

  const bad = validateRegistration({ name: '', email: 'x', phone: '1', consent: false });
  assert.deepEqual(Object.keys(bad.errors).sort(), ['consent', 'email', 'name', 'phone']);
});

test('баркод на картата', () => {
  const serial = '3f2a9c1e-5b7d-4e8a-9c21-7d4e5f6a8b90';
  assert.equal(parseQrPayload(qrPayload(serial)), serial);
  assert.equal(parseQrPayload('https://example.com'), null);
  assert.equal(parseQrPayload(undefined), null);
});
