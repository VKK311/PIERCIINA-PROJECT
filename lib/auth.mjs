import { createHmac, timingSafeEqual } from 'node:crypto';
import { config } from './config.mjs';

const SESSION_DAYS = 30;

const sign = (data) => createHmac('sha256', config.admin.sessionSecret).update(data).digest('base64url');

const safeEqual = (a, b) => {
  const x = Buffer.from(String(a));
  const y = Buffer.from(String(b));
  return x.length === y.length && timingSafeEqual(x, y);
};

export function login(email, password) {
  const { admin } = config;
  if (!admin.password || !admin.sessionSecret) throw new Error('ADMIN_PASSWORD / SESSION_SECRET are not set');
  const emailOk = safeEqual(String(email ?? '').trim().toLowerCase(), admin.email.toLowerCase());
  const passwordOk = safeEqual(password ?? '', admin.password);
  if (!emailOk || !passwordOk) return null;
  const payload = Buffer.from(JSON.stringify({ sub: admin.email, exp: Date.now() + SESSION_DAYS * 864e5 })).toString('base64url');
  return `${payload}.${sign(payload)}`;
}

export function verify(req) {
  if (!config.admin.sessionSecret) return false;
  const token = (req.headers.get('authorization') ?? '').replace(/^Bearer\s+/i, '');
  const [payload, signature] = token.split('.');
  if (!payload || !signature || !safeEqual(signature, sign(payload))) return false;
  try {
    return JSON.parse(Buffer.from(payload, 'base64url').toString()).exp > Date.now();
  } catch {
    return false;
  }
}
