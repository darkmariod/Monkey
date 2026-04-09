-- =============================================
-- SCHEMA: Sistema de Pedidos WhatsApp IA
-- Ejecutar en Supabase > SQL Editor
-- =============================================

-- 1. SABORES (ingredientes / variedades)
create table if not exists sabores (
  id uuid default gen_random_uuid() primary key,
  nombre text not null,
  activo boolean default true,
  created_at timestamptz default now()
);

-- 2. PRODUCTOS (con precios)
create table if not exists productos (
  id uuid default gen_random_uuid() primary key,
  nombre text not null,
  precio numeric(10,2) not null default 0,
  activo boolean default true,
  created_at timestamptz default now()
);

-- 3. PEDIDOS
create table if not exists pedidos (
  id uuid default gen_random_uuid() primary key,
  cliente_nombre text not null default 'Cliente',
  cliente_telefono text,
  items jsonb not null default '[]',
  total numeric(10,2) not null default 0,
  estado text not null default 'pendiente'
    check (estado in ('pendiente', 'confirmado', 'cancelado')),
  notas text,
  created_at timestamptz default now()
);

-- 4. PUSH SUBSCRIPTIONS (para notificaciones)
create table if not exists push_subscriptions (
  id uuid default gen_random_uuid() primary key,
  subscription jsonb not null,
  created_at timestamptz default now()
);

-- =============================================
-- DATOS DE EJEMPLO
-- =============================================

insert into sabores (nombre, activo) values
  ('Carne cortada a cuchillo', true),
  ('Jamón y queso', true),
  ('Pollo con verduras', true),
  ('Humita', true),
  ('Caprese', true),
  ('Acelga y queso', true);

insert into productos (nombre, precio, activo) values
  ('Empanada individual', 350, true),
  ('Docena de empanadas', 3800, true),
  ('Media docena', 1950, true);

insert into pedidos (cliente_nombre, cliente_telefono, items, total, estado, created_at) values
  ('María González', '+5491112345678',
   '[{"sabor":"Carne cortada a cuchillo","cantidad":6},{"sabor":"Jamón y queso","cantidad":6}]',
   3800, 'confirmado', now() - interval '2 hours'),
  ('Juan Pérez', '+5491187654321',
   '[{"sabor":"Pollo con verduras","cantidad":4},{"sabor":"Humita","cantidad":2}]',
   2100, 'pendiente', now() - interval '30 minutes'),
  ('Ana Rodríguez', '+5491198765432',
   '[{"sabor":"Caprese","cantidad":12}]',
   3800, 'pendiente', now() - interval '10 minutes');

-- =============================================
-- ROW LEVEL SECURITY (opcional, para producción)
-- =============================================
-- alter table pedidos enable row level security;
-- alter table sabores enable row level security;
-- alter table productos enable row level security;

-- Política pública de lectura (para el bot de n8n):
-- create policy "Lectura pública" on sabores for select using (true);
-- create policy "Inserción pública" on pedidos for insert with check (true);
