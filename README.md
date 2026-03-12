# 🚀 FastAPI University Project

**Modern backend** with FastAPI demonstrating:

- REST APIs for tasks, users, items, orders  
- JWT Authentication  
- Async operations & background tasks  
- HTML pages with Jinja2  
- Static files (CSS/JS/images)  
- CORS middleware

---

## 🔐 Auth (JWT)

- **POST `/auth/token`** → login & get token  
- Include token in `Authorization: Bearer <token>` for protected routes  

**Example request:**

```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=anna&password=123
🌐 Endpoints

GET / → root test

GET /home → HTML page with dynamic items

GET /items/{id} → fetch item by id

POST /orders → create order

GET /weather/{city} → async fetch weather

POST /register → background task (send email)

🖥️ HTML & Static

Templates: /templates/index.html

Static: /static/style.css, /static/script.js

Access static: http://127.0.0.1:8000/static/style.css

⚡ Async & Background Tasks

async def → non-blocking I/O

BackgroundTasks → tasks run after response

🧪 Run Locally
git clone <repo-url>
cd fastapi-university-project
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose httpx jinja2 aiofiles
uvicorn main:app --reload
