# Sistema de Pedidos — Panel Vanilla JS

Panel de gestión de pedidos en HTML + CSS + JS puro, con Supabase como backend.

## Archivos

- `index.html` — El panel completo (una sola página)
- `supabase-schema.sql` — Schema de la base de datos

## Setup en 3 pasos

### 1. Crear proyecto en Supabase

1. Ve a https://supabase.com y crea una cuenta/proyecto gratis
2. En el panel de Supabase, abre **SQL Editor**
3. Pega el contenido de `supabase-schema.sql` y ejecútalo
4. Esto crea las tablas `sabores`, `productos`, `pedidos` y carga datos de ejemplo

### 2. Obtener credenciales

En Supabase: **Settings → API**

- `Project URL` → algo como `https://xxxx.supabase.co`
- `anon / public key` → el JWT largo

### 3. Abrir el panel

1. Abre `index.html` en tu navegador (doble clic, o con un servidor local)
2. Pega la URL y la Anon Key de Supabase
3. Clic en **Conectar**

¡Listo! Las credenciales quedan guardadas en el navegador.

---

## Bot de WhatsApp (n8n)

El bot se conecta a la misma base de datos Supabase. Necesitas:

1. **Evolution API** — para recibir/enviar mensajes de WhatsApp
2. **n8n** — para el flujo de automatización

El workflow de n8n debe:
- Recibir mensajes via webhook (Evolution API)
- Consultar sabores activos en Supabase: `GET /rest/v1/sabores?activo=eq.true`
- Insertar el pedido en Supabase: `POST /rest/v1/pedidos`

El panel recibirá el pedido en tiempo real por Supabase Realtime.

---

## Funcionalidades del panel

- **Dashboard** — pedidos de hoy, ingresos, confirmados/pendientes, actualización en tiempo real
- **Pedidos** — historial con filtros por fecha (hoy/ayer/semana/todo), estado y búsqueda por nombre
- **Menú** — CRUD completo de sabores y productos con precios
- **Estadísticas** — ingresos, tasa de confirmación, pedidos por día y top sabores

## Stack

| Capa | Tecnología |
|---|---|
| Frontend | HTML + CSS + JS puro (sin frameworks) |
| Base de datos | Supabase (PostgreSQL + Realtime) |
| WhatsApp bot | n8n + Evolution API (externo) |
