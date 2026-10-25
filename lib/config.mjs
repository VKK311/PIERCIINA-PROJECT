const env = (key, fallback) => {
  const value = process.env[key];
  return value === undefined || value === '' ? fallback : value;
};

export const config = {
  siteUrl: env('SITE_URL', 'http://localhost:8888').replace(/\/$/, ''),
  stampsForReward: 5,

  card: {
    title: 'Pierciina Loyalty Card',
    organization: 'Pierciina',
    bg: env('CARD_BG_COLOR', '#111111'),
    fg: env('CARD_FG_COLOR', '#FFFFFF'),
    label: env('CARD_LABEL_COLOR', '#F7C948'),
    star: env('CARD_STAR_COLOR', '#F7C948'),
  },

  studio: {
    address: 'ul. "Graf Ignatiev" 74, 1142 Sofia',
    lat: Number(env('STUDIO_LAT', '42.6885')),
    lng: Number(env('STUDIO_LNG', '23.3265')),
  },

  admin: {
    email: env('ADMIN_EMAIL', 'pierciina1@gmail.com'),
    password: env('ADMIN_PASSWORD'),
    sessionSecret: env('SESSION_SECRET'),
  },

  supabase: {
    url: env('SUPABASE_URL'),
    serviceKey: env('SUPABASE_SERVICE_ROLE_KEY'),
    secretsBucket: env('SECRETS_BUCKET', 'wallet-secrets'),
    secretsDir: env('LOCAL_SECRETS_DIR'),
  },

  apple: {
    passTypeId: env('APPLE_PASS_TYPE_ID', 'pass.com.pierciina.loyalty'),
    teamId: env('APPLE_TEAM_ID'),
    keyPassphrase: env('APPLE_SIGNER_KEY_PASSPHRASE'),
  },

  google: {
    issuerId: env('GOOGLE_ISSUER_ID'),
  },

  brevo: {
    apiKey: env('BREVO_API_KEY'),
    senderEmail: env('BREVO_SENDER_EMAIL', 'pierciina1@gmail.com'),
  },
};

/** Съдържанието на баркода върху картата. */
export const qrPayload = (serial) => `PIERCIINA:${serial}`;

/** Връща serial от сканиран код или null, ако кодът не е на Pierciina. */
export function parseQrPayload(code) {
  const match = /^PIERCIINA:([0-9a-f-]{36})$/i.exec(String(code ?? '').trim());
  return match ? match[1].toLowerCase() : null;
}
