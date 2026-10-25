# Pierciina Loyalty Card

Дигитална карта за лоялност в Apple Wallet и Google Wallet: **5 звезди = 50% отстъпка за 6-ия пиърсинг**.
Без каса, плащания, цени и услуги — само един админ, който сканира картата и решава кога да даде звезда.

## Как работи

1. Клиентът сканира QR кода за регистрация (стикер на рецепцията, екран или Instagram).
2. Попълва 3 полета: име, имейл, телефон (+ съгласие по GDPR).
3. Натиска **Add to Apple Wallet** (или **Add to Google Wallet** на Android).
4. В студиото админът отваря `/admin.html`, сканира QR кода от картата → **+1 звезда** автоматично.
   Два пиърсинга в едно посещение = две сканирания. Грешна звезда се отменя с един бутон.
5. При 5 звезди картата показва „50% OFF your next piercing“, клиентът получава известие,
   а админът — имейл. При следващото сканиране админът натиска **Наградата е използвана** и картата се нулира.

| Страница | За кого |
| --- | --- |
| `/` | Регистрация на клиента |
| `/card.html?id=…` | Бутоните за Wallet след регистрация |
| `/admin.html` | Скенер и списък с клиенти (вход с имейл и парола) |
| `/qr.html` | QR код за регистрация, готов за печат |
| `/privacy.html` | Политика за поверителност |

### Решения от въпросника

- Карта: **Pierciina Loyalty Card**, на английски, без задна страна; отпред — брой звезди и колко остават до наградата.
- Звездите не изтичат. Регистрацията започва от 0 звезди.
- Една карта на телефон, без пароли. Нова регистрация със същия телефон архивира старата карта (започва от 0).
- Известия: имейл до `pierciina1@gmail.com` при нова карта и при 5 звезди; клиентът получава известие
  само при отключена награда (не при всеки печат).
- Картата се показва на заключения екран близо до ул. „Граф Игнатиев“ 74, София.

## Технологии

- **Netlify** — сайтът (`public/`) и сървърните функции (`netlify/functions/`).
- **Supabase** — базата данни (`supabase/migrations/001_init.sql`) и частен bucket за сертификатите.
- **Apple Wallet** — `.pkpass`, подписан с Pass Type ID сертификат; обновяване през Apple web service + APNs.
- **Google Wallet** — Loyalty class/object през Google Wallet API (по избор).
- **Brevo** — имейлите до админа (по избор).

## Пускане

### 1. Supabase

1. Създайте проект в регион в ЕС (напр. Frankfurt).
2. В SQL Editor изпълнете `supabase/migrations/001_init.sql`.
3. Запишете **Project URL** и **service_role** ключа (Settings → API).

### 2. Apple Wallet (задължително)

Нужен е платен Apple Developer Program акаунт (около 99 USD годишно) на личния Apple ID.

1. [developer.apple.com](https://developer.apple.com/account/resources/identifiers/list/passTypeId) →
   Identifiers → **Pass Type IDs** → `pass.com.pierciina.loyalty`.
2. Към него създайте сертификат (CSR от Keychain Access на Mac) и го изтеглете като `pass.cer`.
3. Отворете го в Keychain и експортирайте сертификата с ключа като `pass.p12` (с парола).
4. Изтеглете **Apple WWDR G4** сертификата от [apple.com/certificateauthority](https://www.apple.com/certificateauthority/).
5. Конвертирайте в PEM:

   ```sh
   openssl pkcs12 -in pass.p12 -clcerts -nokeys -out signerCert.pem -legacy
   openssl pkcs12 -in pass.p12 -nocerts -out signerKey.pem -legacy   # задайте парола за ключа
   openssl x509 -inform der -in AppleWWDRCAG4.cer -out wwdr.pem
   ```

6. Качете `signerCert.pem`, `signerKey.pem` и `wwdr.pem` в Supabase Storage, bucket **wallet-secrets**
   (създава се от миграцията, частен е). Сертификатите не се пазят в git.

### 3. Google Wallet (за Android)

1. [Google Pay & Wallet Console](https://pay.google.com/business/console) → Google Wallet API → вземете **Issuer ID**.
2. В Google Cloud включете **Google Wallet API**, създайте service account и JSON ключ.
3. Добавете имейла на service account-а като потребител в Wallet Console.
4. Качете JSON файла като `google-service-account.json` в bucket **wallet-secrets**.

Докато Google не одобри профила за публикуване, картата могат да запазват само тестовите акаунти.

### 4. Brevo (имейли до админа)

Създайте API ключ и потвърдете подателя `pierciina1@gmail.com` (Senders & IP).

### 5. Netlify

1. Нов сайт от това репо (публикува `public/`, функциите се откриват автоматично).
2. Добавете променливите от `.env.example` (Site configuration → Environment variables).
   Задължителни: `SITE_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `ADMIN_PASSWORD`,
   `SESSION_SECRET`, `APPLE_TEAM_ID`, `APPLE_SIGNER_KEY_PASSPHRASE`.
3. Вържете поддомейн, напр. `card.pierciina.com`. Apple Wallet изисква HTTPS.
4. Отпечатайте `/qr.html` за рецепцията.

### 6. Лого и цветове

В момента картата е с временна визия: жълта звезда на черен фон.

- `pass-assets/logo.png` — логото с прозрачен фон (мин. 480×150 px), показва се горе вляво на картата.
- `pass-assets/icon.png` — квадратна иконка (мин. 114×114 px) за известията.
- `public/assets/logo.svg` — логото за страниците.
- Цветовете от pierciina.com → `CARD_BG_COLOR`, `CARD_FG_COLOR`, `CARD_LABEL_COLOR`, `CARD_STAR_COLOR`.

Бутоните „Add to Apple/Google Wallet“ са временни; преди старта ги сменете с официалните значки
от [Apple](https://developer.apple.com/wallet/add-to-apple-wallet-guidelines/) и
[Google](https://developers.google.com/wallet/generic/resources/brand-guidelines).

## Разработка

```sh
npm install
npm test          # правила, телефони, съдържание на .pkpass, изображения, Google обект
npx netlify dev   # локално, с .env файл (LOCAL_SECRETS_DIR=./certs чете сертификатите от папка)
```
