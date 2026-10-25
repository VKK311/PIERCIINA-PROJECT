import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import sharp from 'sharp';
import { config } from './config.mjs';

// Без текст в SVG: във функциите на Netlify няма шрифтове. Името идва от logoText на картата.
const STAR = 'M50 4l13.5 29.6 32.4 3.6-24.2 21.9 6.8 31.9L50 74.7 21.5 91l6.8-31.9L4.1 37.2l32.4-3.6z';

const star = (x, y, size, filled, color) =>
  `<path d="${STAR}" transform="translate(${x} ${y}) scale(${size / 100})" ` +
  (filled
    ? `fill="${color}"/>`
    : `fill="none" stroke="${color}" stroke-opacity="0.55" stroke-width="${(4 * 100) / size}"/>`);

/** Лентата с печатите: total звезди, първите `stamps` са запълнени. */
export function stripSvg(stamps, { width = 750, height = 246, total = config.stampsForReward } = {}) {
  const { bg, star: color } = config.card;
  const size = Math.min(height * 0.5, (width * 0.8) / total);
  const gap = (width - size * total) / (total + 1);
  const y = (height - size) / 2;
  const stars = Array.from({ length: total }, (_, i) => star(gap + i * (size + gap), y, size, i < stamps, color)).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}"><rect width="100%" height="100%" fill="${bg}"/>${stars}</svg>`;
}

export function iconSvg(size) {
  const { bg, star: color } = config.card;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}"><rect width="100%" height="100%" fill="${bg}"/>${star(size * 0.15, size * 0.15, size * 0.7, true, color)}</svg>`;
}

export function logoSvg(height) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${height}" height="${height}">${star(0, 0, height, true, config.card.star)}</svg>`;
}

const png = (svg) => sharp(Buffer.from(svg)).png().toBuffer();

/** Истинското лого (pass-assets/logo.png), ако е качено; иначе — звездата. */
function customAsset(name) {
  const path = join(process.cwd(), 'pass-assets', name);
  return existsSync(path) ? readFileSync(path) : null;
}

async function logoPng(height) {
  const custom = customAsset('logo.png');
  if (custom) return sharp(custom).resize({ height, width: height * 3.2, fit: 'inside' }).png().toBuffer();
  return png(logoSvg(height));
}

async function iconPng(size) {
  const custom = customAsset('icon.png');
  if (custom) return sharp(custom).resize(size, size, { fit: 'contain', background: config.card.bg }).png().toBuffer();
  return png(iconSvg(size));
}

const cache = new Map();
const cached = (key, make) => {
  if (!cache.has(key)) cache.set(key, make());
  return cache.get(key);
};

export const stripPng = (stamps, width, height) =>
  cached(`strip-${stamps}-${width}x${height}`, () => png(stripSvg(stamps, { width, height })));

/** Файловете за Apple pass (размери по Apple Wallet Human Interface Guidelines). */
export async function applePassImages(stamps) {
  const [icon, icon2x, icon3x, logo, logo2x, strip, strip2x] = await Promise.all([
    cached('icon-29', () => iconPng(29)),
    cached('icon-58', () => iconPng(58)),
    cached('icon-87', () => iconPng(87)),
    cached('logo-50', () => logoPng(50)),
    cached('logo-100', () => logoPng(100)),
    stripPng(stamps, 375, 123),
    stripPng(stamps, 750, 246),
  ]);
  return {
    'icon.png': icon,
    'icon@2x.png': icon2x,
    'icon@3x.png': icon3x,
    'logo.png': logo,
    'logo@2x.png': logo2x,
    'strip.png': strip,
    'strip@2x.png': strip2x,
  };
}

/** Публични изображения за Google Wallet (Google ги тегли по URL). */
export async function publicImage(name) {
  if (name === 'logo.png') return cached('glogo', () => iconPng(660));
  const match = /^strip-(\d)\.png$/.exec(name);
  if (match && Number(match[1]) <= config.stampsForReward) return stripPng(Number(match[1]), 1032, 336);
  return null;
}
