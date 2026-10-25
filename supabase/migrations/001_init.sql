-- Pierciina Loyalty Card: клиенти, история на печатите и регистрации на Apple устройства.
-- Достъпът е само през сървърните функции със service role ключа; RLS е включен без политики,
-- така че публичният (anon) ключ няма достъп до нищо.

create table if not exists clients (
  id            uuid primary key default gen_random_uuid(),
  serial        uuid not null unique default gen_random_uuid(),
  auth_token    text not null default replace(gen_random_uuid()::text || gen_random_uuid()::text, '-', ''),
  name          text not null,
  email         text not null,
  phone         text not null,
  stamps        int  not null default 0 check (stamps >= 0),
  rewards_redeemed int not null default 0,
  active        boolean not null default true,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

create index if not exists clients_phone_idx on clients (phone) where active;
create index if not exists clients_updated_idx on clients (updated_at);

create table if not exists stamp_events (
  id         bigint generated always as identity primary key,
  client_id  uuid not null references clients (id) on delete cascade,
  action     text not null check (action in ('stamp', 'remove', 'redeem')),
  stamps_after int not null,
  created_at timestamptz not null default now()
);

create index if not exists stamp_events_client_idx on stamp_events (client_id, created_at desc);

create table if not exists apple_registrations (
  device_library_id text not null,
  pass_type_id      text not null,
  serial            uuid not null references clients (serial) on delete cascade,
  push_token        text not null,
  created_at        timestamptz not null default now(),
  primary key (device_library_id, pass_type_id, serial)
);

create index if not exists apple_registrations_serial_idx on apple_registrations (serial);

alter table clients enable row level security;
alter table stamp_events enable row level security;
alter table apple_registrations enable row level security;

-- Частен bucket за сертификатите на Apple и ключа на Google (файловете се качват ръчно).
insert into storage.buckets (id, name, public)
values ('wallet-secrets', 'wallet-secrets', false)
on conflict (id) do nothing;
