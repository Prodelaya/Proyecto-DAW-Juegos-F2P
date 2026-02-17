# FreeToGame API — Documentación

> **Documentación relacionada:** [Arquitectura](01-Arquitectura.md) · [Estructura y archivos](02-Estructura-y-archivos.md) · [Roadmap Backend](03-Roadmap-backend.md) · [Roadmap Frontend](04-Roadmap-frontend.md) · [Memoria y defensa](05-Memoria-y-defensa.md)

---

## Overview

**Free-To-Play Games Database API** — Discover the Best Free-To-Play Games with Ease!

Access programmatically the best free-to-play games and free MMO games! This API provides access to a comprehensive database of free-to-play games and free MMO games. You can use this API to retrieve information about free games, such as their title, genre, description and more.

The FreeToGame API is available for everyone to use without any restrictions. Please note our API is free to use as long as you attribute FreeToGame.com as the source of the data.

### Key Features

| Feature | Detalle |
|---------|---------|
| 💰 **100% Free forever** | Sin costes ni restricciones |
| 🎮 **+400 juegos** | Acceso a más de 400 juegos free-to-play |
| 📋 **Metadata detallada** | Géneros, developers, publishers, fechas, webs oficiales y más |
| 🔓 **Sin autenticación** | No requiere API key ni cuenta |
| 🏢 **Uso comercial** | Libre para uso personal y comercial |
| ⚡ **Fácil integración** | Resultados JSON con simples peticiones HTTP GET |

---

## Getting Started

1. **Authentication:** No se requiere autenticación. Simplemente hacer peticiones HTTP a los endpoints.
2. **Base URL:** `https://www.freetogame.com/api`
3. **Endpoints disponibles:**
   - `/games` — Lista de todos los juegos free-to-play
   - `/game?id={game_id}` — Detalles de un juego específico por ID
   - `/games?category={category_name}` — Juegos por género
   - `/games?platform={platform_name}` — Juegos por plataforma
   - `/games?sort-by={sort_name}` — Ordenar por fecha, alfabético o relevancia

---

## Endpoints & Examples

### Lista completa de juegos

```
GET https://www.freetogame.com/api/games
```

### Juegos por plataforma

```
GET https://www.freetogame.com/api/games?platform=pc
```

Valores de `platform`: `pc`, `browser`, `all`

### Juegos por categoría o tag

```
GET https://www.freetogame.com/api/games?category=shooter
```

Valores de `category`: `mmorpg`, `shooter`, `pvp`, `mmofps`, y más.

### Ordenar juegos

```
GET https://www.freetogame.com/api/games?sort-by=alphabetical
```

Valores de `sort-by`: `release-date`, `popularity`, `alphabetical`, `relevance`

### Combinar filtros (plataforma + categoría + orden)

```
GET https://www.freetogame.com/api/games?platform=browser&category=mmorpg&sort-by=release-date
```

### Filtrar por múltiples tags

```
GET https://www.freetogame.com/api/filter?tag=3d.mmorpg.fantasy.pvp&platform=pc
```

Tags separados por `.`, ej: `mmorpg`, `shooter`, `pvp`, `mmofps`. Opcionalmente se pueden usar los parámetros `platform` y `sort`.

### Detalles de un juego específico

```
GET https://www.freetogame.com/api/game?id=452
```

### Game recommendations

```
Coming Soon
```

---

## Respuestas de ejemplo y campos que usamos

### `/games` — Respuesta (array de objetos)

Cada elemento del array tiene esta estructura:

```json
{
  "id": 540,
  "title": "Overwatch",
  "thumbnail": "https://www.freetogame.com/g/540/thumbnail.jpg",
  "short_description": "A hero-focused first-person team shooter from Blizzard Entertainment.",
  "game_url": "https://www.freetogame.com/open/overwatch",
  "genre": "Shooter",
  "platform": "PC (Windows)",
  "publisher": "Activision Blizzard",
  "developer": "Blizzard Entertainment",
  "release_date": "2022-10-04",
  "freetogame_profile_url": "https://www.freetogame.com/overwatch"
}
```

### `/game?id=540` — Respuesta (objeto único, más completo)

```json
{
  "id": 540,
  "title": "Overwatch",
  "thumbnail": "https://www.freetogame.com/g/540/thumbnail.jpg",
  "status": "Live",
  "short_description": "A hero-focused first-person team shooter from Blizzard Entertainment.",
  "description": "The tale of the hero organization Overwatch continues in Overwatch 2...",
  "game_url": "https://www.freetogame.com/open/overwatch",
  "genre": "Shooter",
  "platform": "Windows",
  "publisher": "Activision Blizzard",
  "developer": "Blizzard Entertainment",
  "release_date": "2022-10-04",
  "freetogame_profile_url": "https://www.freetogame.com/overwatch",
  "minimum_system_requirements": {
    "os": "Windows 10 64-bit",
    "processor": "Intel Core i3 or AMD Phenom X3 8650",
    "memory": "6 GB RAM",
    "graphics": "NVIDIA GeForce GTX 600 series, AMD Radeon HD 7000 series",
    "storage": "50 GB"
  },
  "screenshots": [
    { "id": 1334, "image": "https://www.freetogame.com/g/540/overwatch-2-1.jpg" },
    { "id": 1335, "image": "https://www.freetogame.com/g/540/overwatch-2-2.jpg" },
    { "id": 1336, "image": "https://www.freetogame.com/g/540/overwatch-2-3.jpg" }
  ]
}
```

### Estrategia de uso en el proyecto

| Endpoint | Cuándo se llama | Qué campos extraemos | Mapeo al modelo `Game` |
|----------|----------------|----------------------|------------------------|
| `/games` | Seed — 1ª llamada (1 request, ~400 resultados) | id, title, thumbnail, short_description, genre, platform, developer, publisher, release_date, game_url, freetogame_profile_url | `api_id` ← id, resto campos 1:1 |
| `/game?id={id}` | Seed — por cada juego (~400 requests) | status, description, minimum_system_requirements (os, processor, memory, graphics, storage), screenshots | `status`, `description`, `req_os`, `req_processor`, `req_memory`, `req_graphics`, `req_storage`, `screenshots` (JSON) |

> [!IMPORTANT]
> Ambos endpoints se llaman durante el seed. El proceso tarda ~60-90 segundos por el rate-limit de la API (10 req/s). Se usa `time.sleep(0.15)` entre llamadas al endpoint `/game?id`. No todos los juegos tienen `minimum_system_requirements` (juegos de navegador no lo incluyen), esos campos quedan como NULL.

---

## Response Format

Las respuestas se devuelven en **formato JSON** con la información relevante según el endpoint accedido.

---

## CORS Support

Si necesitas cross-origin resource sharing, puedes acceder a la API vía RapidAPI:
`https://rapidapi.com/digiwalls/api/free-to-play-games-database`

---

## Rate Limits

> [!WARNING]
> Máximo **10 requests por segundo**. Evitar superar este límite.

---

## Códigos de respuesta

| Código | Significado |
|--------|-------------|
| `200` | ✅ Success |
| `404` | ❌ Object not found — Game o endpoint no encontrado |
| `500` | ⚠️ Server error — Error inesperado en el servidor |
