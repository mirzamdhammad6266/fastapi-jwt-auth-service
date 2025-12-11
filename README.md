# FastAPI JWT Auth Service

A **FastAPI-based authentication service** that demonstrates how to implement user registration, login, and protected routes using **JSON Web Tokens (JWT)**.  
This project is intentionally small and focused so it can be used both as a learning resource and as a portfolio example for backend authentication patterns in Python.

---

## 🔐 Features

- `/register` endpoint to create a new user with a **hashed password** (demo in-memory store).
- `/login` endpoint using **OAuth2 password flow** that returns a signed **JWT access token**.
- `/me` protected endpoint that requires a valid `Authorization: Bearer <token>` header.
- `/health` endpoint for basic uptime checks.
- Password hashing handled by **Passlib (bcrypt)**.
- JWT tokens signed with **python-jose** using the `HS256` algorithm.
- Clear separation between **auth logic** (`auth.py`), **schemas** (`schemas.py`), and the **FastAPI app** (`main.py`).
- Easy to extend with refresh tokens, roles/permissions, or a real database (PostgreSQL, etc.).

---

## 🗂 Project Structure

```text
fastapi-jwt-auth-service/
├─ app/
│  ├─ main.py        # FastAPI app, routes, dependencies
│  ├─ auth.py        # Auth helpers, hashing, JWT encode/decode
│  └─ schemas.py     # Pydantic models for users and tokens
├─ requirements.txt  # Python dependencies
└─ README.md         # Project documentation
```

---

## Run Locally
```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/fastapi-jwt-auth-service.git
cd fastapi-jwt-auth-service

# 2. (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the FastAPI server
uvicorn app.main:app --reload
```

---

## 🔌 API Endpoints

---

### **1. POST /register – Create a user**

#### Request body  
```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

#### Example Responses
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "role": "user"
}
```

---

### **2. POST /login – Obtain JWT token**
Uses OAuth2 password flow. In Swagger UI, click Authorize and use:
-username: your email
-password: the password you registered with

#### Curl-style example
```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=strongpassword123"
```

#### Example response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### **3. GET /me – Protected user profile**
Send the access token in the Authorization header:
```http
GET /me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
#### Example response
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "role": "user"
}
```

---

### **4. GET /health – Health check**
```http
GET /health
```

#### Response
```json
{ "status": "ok" }
```

---

## 🧩 Extending This Service
To make this closer to a production-ready auth system, you can integrate:

- **A real database (PostgreSQL + SQLAlchemy) for persisting users.**
- **Refresh tokens and token revocation/blacklist.**
- **Role-based access control (RBAC) for admin vs user endpoints.**
- **Logging, metrics, and request tracing.**

The current implementation is intentionally simple so reviewers can quickly understand the flow during code review or interviews.

---

## Tech Stack

- Python 3.10+  
- FastAPI  
- Passlib (bcrypt) 
- Uvicorn(ASGI server) 
- Pydantic
- Python-jose for JWT
