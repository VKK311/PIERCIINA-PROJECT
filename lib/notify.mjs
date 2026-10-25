import { config } from './config.mjs';

const escape = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

/** Имейл до админа през Brevo. Без BREVO_API_KEY просто се пропуска. */
export async function emailAdmin(subject, lines) {
  if (!config.brevo.apiKey) return;
  const res = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: { 'api-key': config.brevo.apiKey, 'content-type': 'application/json', accept: 'application/json' },
    body: JSON.stringify({
      sender: { name: 'Pierciina Loyalty Card', email: config.brevo.senderEmail },
      to: [{ email: config.admin.email }],
      subject,
      htmlContent: `<div style="font-family:sans-serif">${lines.map((l) => `<p>${escape(l)}</p>`).join('')}</div>`,
    }),
  });
  if (!res.ok) console.error('Brevo email failed', res.status, await res.text());
}

export const clientLines = (c) => [`Име: ${c.name}`, `Телефон: ${c.phone}`, `Имейл: ${c.email}`];
