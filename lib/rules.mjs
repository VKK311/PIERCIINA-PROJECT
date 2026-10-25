import { config } from './config.mjs';

const N = config.stampsForReward;

/**
 * Правилата на картата, без база данни:
 * - stamp: +1 печат; при 5 печата наградата е отключена и следващите сканирания не добавят.
 * - remove: −1 печат (поправка на грешка).
 * - redeem: използване на наградата (50% за 6-ия пиърсинг) — картата се нулира.
 */
export function applyAction(stamps, action) {
  switch (action) {
    case 'stamp': {
      if (stamps >= N) return { stamps, changed: false, result: 'reward_ready' };
      const next = stamps + 1;
      return { stamps: next, changed: true, result: next >= N ? 'reward_unlocked' : 'stamped' };
    }
    case 'remove':
      if (stamps <= 0) return { stamps: 0, changed: false, result: 'nothing_to_remove' };
      return { stamps: stamps - 1, changed: true, result: 'removed' };
    case 'redeem':
      if (stamps < N) return { stamps, changed: false, result: 'reward_not_ready' };
      return { stamps: 0, changed: true, result: 'redeemed' };
    default:
      throw new Error(`Unknown action: ${action}`);
  }
}

export const isRewardReady = (stamps) => stamps >= N;

/** Текстът под печатите на картата (на английски, както е избрано във въпросника). */
export function progressText(stamps) {
  if (isRewardReady(stamps)) return '50% OFF your next piercing';
  const left = N - stamps;
  return `${left} more ${left === 1 ? 'star' : 'stars'} to 50% off`;
}

export function validateRegistration(body) {
  const name = String(body?.name ?? '').trim().replace(/\s+/g, ' ');
  const email = String(body?.email ?? '').trim().toLowerCase();
  const phone = normalizePhone(body?.phone);
  const errors = {};
  if (name.length < 2 || name.length > 80) errors.name = 'Моля, въведете име.';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 120) errors.email = 'Невалиден имейл.';
  if (!phone) errors.phone = 'Невалиден телефон.';
  if (body?.consent !== true) errors.consent = 'Необходимо е съгласие.';
  return { ok: Object.keys(errors).length === 0, errors, value: { name, email, phone } };
}

/** Нормализира български и международни номера: 0888 123 456 → +359888123456. */
export function normalizePhone(raw) {
  let digits = String(raw ?? '').replace(/[^\d+]/g, '');
  if (digits.startsWith('00')) digits = `+${digits.slice(2)}`;
  if (/^0\d{8,9}$/.test(digits)) digits = `+359${digits.slice(1)}`;
  if (/^359\d{8,9}$/.test(digits)) digits = `+${digits}`;
  return /^\+\d{8,15}$/.test(digits) ? digits : null;
}
