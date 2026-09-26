# Users REST API — Flask + MySQL

A modular, API-first REST backend built with **Flask** and **MySQL**. Supports full CRUD operations on users, search, pagination, validation, error handling, and JWT authentication.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Assumptions](#assumptions)
- [Short Answers](#short-answers)
- [AI Usage Declaration](#ai-usage-declaration)

---

## Project Structure

```
├── app/
│   ├── __init__.py          # Application factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model (SQLAlchemy)
│   │   └── admin.py         # AdminUser model for JWT
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py   # /users endpoints
│   │   └── auth_routes.py   # /auth endpoints (JWT)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py  # Business logic for users
│   │   └── auth_service.py  # Business logic for auth
│   └── utils/
│       ├── __init__.py
│       ├── validators.py    # Email & field validation
│       └── error_handlers.py
├── run.py                   # Entry point
├── schema.sql               # MySQL schema (reference)
├── requirements.txt
├── .env                     # Environment variables
├── .gitignore
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Create & activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up MySQL database

Log in to MySQL and create the database:

```sql
CREATE DATABASE IF NOT EXISTS users CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or run the provided schema file:

```bash
mysql -u root -p < schema.sql
```

### 5. Configure environment variables

Edit the `.env` file with your MySQL credentials:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/users
JWT_SECRET_KEY=change-this-to-a-strong-random-secret
```

### 6. Run the application

```bash
python run.py
```

The server starts at `http://localhost:5000`. Tables are created automatically on first run.

---

## API Endpoints

### Users

#### GET `/users` — Retrieve all users

```bash
curl http://localhost:5000/users
```

**Response** `200 OK`:

```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 1,
        "name": "Vinay",
        "email": "vinay@example.com",
        "role": "admin",
        "created_at": "2026-09-26T13:00:00",
        "updated_at": "2026-09-26T13:00:00"
      }
    ]
  }
}
```

#### GET `/users?search=vinay` — Search by name or email

```bash
curl "http://localhost:5000/users?search=vinay"
```

#### GET `/users?page=1&limit=10` — Paginated results

```bash
curl "http://localhost:5000/users?page=1&limit=10"
```

**Response** `200 OK`:

```json
{
  "success": true,
  "data": {
    "users": [ ... ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "pages": 3,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

#### GET `/users/<id>` — Retrieve user by ID

```bash
curl http://localhost:5000/users/1
```

**Error response** `404`:

```json
{
  "success": false,
  "error": "User not found"
}
```

#### POST `/users` — Create a new user

```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Vinay", "email": "vinay@example.com", "role": "admin"}'
```

**Response** `201 Created`:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Vinay",
    "email": "vinay@example.com",
    "role": "admin",
    "created_at": "2026-09-26T13:00:00",
    "updated_at": "2026-09-26T13:00:00"
  }
}
```

**Validation error** `400`:

```json
{
  "success": false,
  "error": "Missing required field(s): name, email"
}
```

**Duplicate email** `400`:

```json
{
  "success": false,
  "error": "A user with this email already exists"
}
```

#### PUT `/users/<id>` — Update user *(JWT required)*

```bash
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name": "Vinay Kumar"}'
```

#### DELETE `/users/<id>` — Delete user *(JWT required)*

```bash
curl -X DELETE http://localhost:5000/users/1 \
  -H "Authorization: Bearer <token>"
```

---

### Authentication (Bonus)

#### POST `/auth/register` — Register an admin

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret123"}'
```

#### POST `/auth/login` — Get JWT token

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret123"}'
```

**Response** `200 OK`:

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

---

## Database Schema

### Table: `users`

| Column       | Type          | Constraints              |
|-------------|---------------|--------------------------|
| `id`        | INT           | PRIMARY KEY, AUTO_INCREMENT |
| `name`      | VARCHAR(120)  | NOT NULL                 |
| `email`     | VARCHAR(255)  | NOT NULL, UNIQUE         |
| `role`      | VARCHAR(80)   | NOT NULL                 |
| `created_at`| DATETIME      | NOT NULL, DEFAULT NOW    |
| `updated_at`| DATETIME      | NOT NULL, DEFAULT NOW    |

### Table: `admin_users` *(bonus — JWT auth)*

| Column          | Type          | Constraints              |
|----------------|---------------|--------------------------|
| `id`           | INT           | PRIMARY KEY, AUTO_INCREMENT |
| `username`     | VARCHAR(80)   | NOT NULL, UNIQUE         |
| `password_hash`| VARCHAR(255)  | NOT NULL                 |
| `created_at`   | DATETIME      | NOT NULL, DEFAULT NOW    |

---

## Assumptions

1. **Email uniqueness** — Emails are stored in lowercase and must be unique across all users.
2. **Role values** — The `role` field is a free-form string (e.g., "admin", "user", "editor"). No enum restriction is enforced.
3. **Pagination** — Pagination is only applied when the `page` query parameter is provided. Without it, all results are returned.
4. **JWT scope** — JWT authentication protects destructive operations (PUT, DELETE). GET and POST are open for demonstration purposes.
5. **Password storage** — Admin passwords are hashed using Werkzeug's `generate_password_hash` (PBKDF2).

---

## Short Answers

### 1. Why did you choose Flask?

Flask was chosen because it is lightweight, flexible, and ideal for building small-to-medium REST APIs. Unlike Django, Flask does not impose a rigid project structure, allowing for a custom modular layout (`/routes`, `/models`, `/services`) as required by this assignment. Flask also has a rich ecosystem of extensions (SQLAlchemy, JWT, CORS) that can be added as needed without unnecessary overhead.

### 2. How would you scale this system?

- **Horizontal scaling**: Deploy multiple Flask instances behind a load balancer (e.g., Nginx + Gunicorn workers).
- **Database scaling**: Use MySQL read replicas for read-heavy traffic, and connection pooling (e.g., SQLAlchemy pool or PgBouncer-equivalent for MySQL).
- **Caching**: Add Redis for caching frequently accessed user data and reducing database load.
- **Async processing**: Offload long-running tasks (email sending, reports) to a task queue like Celery with Redis/RabbitMQ.
- **Containerisation**: Dockerize the application for consistent deployments, and use Kubernetes for orchestration at scale.
- **API Gateway**: Introduce rate limiting, request throttling, and API versioning via an API gateway.

### 3. What changes would you make for production?

- **Security**: Enforce HTTPS, use strong JWT secrets rotated periodically, implement rate limiting, and add CSRF protection.
- **Configuration**: Use environment-specific configs (dev/staging/prod) and never commit secrets to version control — use a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault).
- **Logging & Monitoring**: Integrate structured logging (e.g., Python `logging` with JSON formatter), application monitoring (e.g., Prometheus + Grafana), and error tracking (e.g., Sentry).
- **Database**: Run database migrations with Flask-Migrate (Alembic) instead of `db.create_all()`, enable SSL for database connections, and set up automated backups.
- **Testing**: Add unit tests, integration tests, and CI/CD pipelines (e.g., GitHub Actions) to run tests on every push.
- **WSGI Server**: Replace Flask's development server with a production WSGI server like Gunicorn or uWSGI.
- **Input sanitisation**: Add stricter input validation and sanitisation to protect against injection attacks.

---

## AI Usage Declaration

- **AI Tools Used**: Google Gemini (Antigravity IDE) was used as a coding assistant during development.
- **AI-Generated Parts**: The initial project scaffolding, boilerplate code structure, README documentation, and code comments were generated with AI assistance.
- **Manual Modifications**: All business logic was reviewed and validated manually. Database schema design decisions, error handling strategy, and API response format were directed by human judgment. The `.env` configuration, Git workflow, and deployment considerations were set up manually.
