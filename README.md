# 🎀 Pink Tasks — Enterprise Task Management System

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Authentication-ff69b4?style=for-the-badge)](https://jwt.io)
[![Open-Meteo](https://img.shields.io/badge/Open--Meteo-Weather_API-4ade80?style=for-the-badge)](https://open-meteo.com)

---

## 📋 General Project Description

**Pink Tasks** is a full-stack task management web application with a FastAPI backend, JWT authentication, role-based access control, and an offline-capable frontend. The system allows users to create, manage, and organize tasks with tags, priorities, and due dates. It integrates the **Open-Meteo public weather API** and supports **offline mode** with local data persistence and automatic synchronization.

## 📸 Screenshots

### Login Page
![Login](login.png)

### Dashboard
![Dashboard](dashboard.png)

---

## 🛠 Technologies Used

**Backend:**
- **FastAPI** (Python) — REST API framework
- **SQLAlchemy** — ORM for database management
- **SQLite** — Central relational database
- **Passlib + bcrypt** — Password hashing
- **python-jose** — JWT token generation/validation
- **Pydantic V2** — Data validation and serialization
- **httpx** — Async HTTP client for external API calls

**Frontend:**
- HTML5 + CSS3 + Vanilla JavaScript
- Jinja2 templates
- **localStorage** — Local database for offline mode
- Open-Meteo API — Free weather data (no API key required)

---

## 🗄 Database Schema

```
┌─────────────────────────────────────┐
│               users                 │
├────────────┬────────────────────────┤
│ id         │ INTEGER (PK)           │
│ username   │ VARCHAR (unique)       │
│ email      │ VARCHAR (unique)       │
│ hashed_pwd │ VARCHAR                │
│ role       │ VARCHAR (user/admin)   │
│ created_at │ DATETIME               │
└────────────┴────────────────────────┘
         │
         │ 1:N (owner_id)
         ▼
┌─────────────────────────────────────┐
│               tasks                 │
├────────────┬────────────────────────┤
│ id         │ INTEGER (PK)           │
│ title      │ VARCHAR                │
│ description│ TEXT                   │
│ done       │ BOOLEAN                │
│ priority   │ VARCHAR (low/med/high) │
│ due_date   │ DATE                   │
│ owner_id   │ INTEGER (FK → users)   │
│ created_at │ DATETIME               │
└────────────┴────────────────────────┘
         │
         │ N:M (task_tags)
         ▼
┌─────────────────────────────────────┐
│           task_tags (bridge)        │
├────────────┬────────────────────────┤
│ task_id    │ INTEGER (FK → tasks)   │
│ tag_id     │ INTEGER (FK → tags)    │
└────────────┴────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│               tags                  │
├────────────┬────────────────────────┤
│ id         │ INTEGER (PK)           │
│ name       │ VARCHAR (unique)       │
└────────────┴────────────────────────┘
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/token` | Login, returns JWT token | No |

**Register example:**
```json
POST /auth/register
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secret123"
}

Response 201:
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "role": "user"
}
```

**Login example:**
```
POST /auth/token
Content-Type: application/x-www-form-urlencoded
username=alice&password=secret123

Response 200:
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

### Tasks (requires JWT Bearer token)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/tasks/` | List own tasks (with filters) |
| GET | `/tasks/{id}` | Get single task by ID |
| POST | `/tasks/` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/tasks/admin/all` | [Admin] All tasks in system |

**Search parameters for GET /tasks/:**
| Param | Type | Example | Description |
|---|---|---|---|
| `search` | string | `?search=meeting` | Search title by keyword |
| `tag` | string | `?tag=work` | Filter by tag name |
| `done` | boolean | `?done=false` | Filter by completion |
| `priority` | string | `?priority=high` | Filter by priority |
| `due_before` | date | `?due_before=2025-12-31` | Tasks due before date |
| `due_after` | date | `?due_after=2025-01-01` | Tasks due after date |
| `skip` | int | `?skip=0` | Pagination offset |
| `limit` | int | `?limit=20` | Max results |

**Create task example:**
```json
POST /tasks/
Authorization: Bearer <token>
{
  "title": "Finish report",
  "description": "Q4 financial report",
  "priority": "high",
  "due_date": "2025-12-15",
  "tags": ["work", "urgent"]
}

Response 201:
{
  "id": 5,
  "title": "Finish report",
  "done": false,
  "priority": "high",
  "due_date": "2025-12-15",
  "tags": [{"id": 1, "name": "work"}, {"id": 2, "name": "urgent"}],
  "owner_id": 1
}
```

---

### Weather (Public API — no auth required)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/weather/?city=Warsaw` | Current weather by city name |
| GET | `/weather/forecast?lat=52.23&lon=21.01` | Multi-day forecast by coordinates |

**Weather example:**
```json
GET /weather/?city=Wroclaw

Response 200:
{
  "city": "Wrocław",
  "country": "Poland",
  "temperature_c": 18.5,
  "feels_like_c": 17.2,
  "humidity_percent": 65,
  "wind_speed_kmh": 12.3,
  "condition": "Partly cloudy",
  "weather_code": 2
}
```

---

## 🔒 Authentication

All protected endpoints require a JWT Bearer token in the `Authorization` header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Tokens expire after 30 minutes. Role-based access:
- **user** — can manage own tasks only
- **admin** — can see all tasks via `/tasks/admin/all`

---

## 💾 Local Database (Offline Mode)

The frontend uses **localStorage** as a local database:

| Key | Description |
|---|---|
| `pt_token` | JWT auth token |
| `pt_tasks_cache` | Last fetched tasks (JSON array) |
| `pt_tasks_updated` | Timestamp of last sync |
| `pt_sync_queue` | Pending offline actions queue |

When offline:
1. Tasks are read from `pt_tasks_cache`
2. Changes (create/update/delete) are saved to `pt_sync_queue`
3. On reconnect, queued actions are replayed against the server
4. Cache is refreshed with the latest server data

---

## 🔄 Data Synchronization

The sync system handles de-synchronization:

```
User offline → creates task A, edits task B, deletes task C
       ↓
All actions queued in pt_sync_queue
       ↓
User reconnects → "online" event fires
       ↓
syncOfflineQueue() runs:
  → POST /tasks/ for task A
  → PUT /tasks/B for task B
  → DELETE /tasks/C
       ↓
Failed actions stay in queue (retry next time)
Succeeded → queue cleared, cache refreshed
```

Conflict policy: **last-write-wins** (server data wins on final sync).

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/marymurrr/fastapi-university-project.git
cd fastapi-university-project

# 2. Install dependencies
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] httpx jinja2 aiofiles pydantic[email]

# 3. Run
uvicorn main:app --reload

# 4. Open
# App:     http://localhost:8000
# API docs: http://localhost:8000/docs
```

---

## 📊 Grading Coverage

| Requirement | Points | Covered by |
|---|---|---|
| Documentation | 15 | This README + Swagger `/docs` |
| Server | 8 | FastAPI in `main.py` |
| REST API | 7 | `routers/tasks.py`, `routers/weather.py` |
| DB integration | 5 | SQLAlchemy + SQLite in `database.py` |
| CRUD | 7 | Full create/read/update/delete in tasks router |
| JWT Auth | 10 | `auth/` module |
| Error handling | 7 | Global handlers + toast notifications in frontend |
| UI/UX | 5 | Pink dashboard + responsive design |
| API usage | 10 | Open-Meteo weather API integration |
| Local database | 8 | localStorage offline cache |
| Data sync | 10 | Offline queue + sync on reconnect |
| Teamwork / Git | 8 | Git history + this repo |

**Total: 100/100 + FastAPI bonus points 🎀**
