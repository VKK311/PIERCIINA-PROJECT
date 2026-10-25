import QRCode from 'qrcode';
import { config as app } from '../../lib/config.mjs';
import { publicImage } from '../../lib/images.mjs';
import { handle, json } from '../../lib/http.mjs';

/**
 * GET /api/img/logo.png, /api/img/strip-0..5.png — изображения за Google Wallet
 * GET /api/img/register-qr.svg — баркодът за регистрация (стикер, екран, Instagram)
 */
export default handle(async (_req, context) => {
  const name = context.params.name;
  if (name === 'register-qr.svg') {
    const svg = await QRCode.toString(`${app.siteUrl}/`, { type: 'svg', margin: 1, errorCorrectionLevel: 'M' });
    return new Response(svg, { headers: { 'content-type': 'image/svg+xml', 'cache-control': 'public, max-age=3600' } });
  }
  const image = await publicImage(name);
  if (!image) return json({ error: 'not_found' }, 404);
  return new Response(image, { headers: { 'content-type': 'image/png', 'cache-control': 'public, max-age=86400' } });
});

export const config = { path: '/api/img/:name' };
