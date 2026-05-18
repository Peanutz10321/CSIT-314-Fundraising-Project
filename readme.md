# Fundraising Platform

This project is an online fundraising platform developed for the **CSIT314 Software Development Methodologies** group project.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Python
- **Frontend:** React 19, Vite
- **Database:** SQLite for local/automated testing, Supabase PostgreSQL for shared/demo database
- **Authentication:** JWT (HS256)
- **Testing:** Pytest
- **CI:** GitHub Actions

## Project Structure

```
CSIT-314-Fundraising-Project/
├── backend/
│   ├── app/
│   │   ├── controllers/        # Business logic layer
│   │   ├── entities/           # SQLAlchemy ORM models
│   │   ├── routes/             # API endpoints
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── middleware/         # JWT auth & role-based access control
│   │   ├── seeds/              # Database seeding scripts
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/                  # Pytest test suite
│   ├── conftest.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                # API client modules
│   │   ├── boundary/           # Page components organized by role
│   │   │   ├── auth/
│   │   │   ├── donee/
│   │   │   ├── fundraiser/
│   │   │   ├── userAdmin/
│   │   │   └── platformManagement/
│   │   ├── components/         # Reusable UI components
│   │   └── App.jsx             # Role-based routing & state
│   ├── package.json
│   └── vite.config.js
└── .github/
    └── workflows/
        └── Ci.yml
```

## User Roles

| Role | Capabilities |
|------|-------------|
| **User Admin** | Manage user accounts and user profiles (create, update, suspend, search) |
| **Fundraiser** | Create, update, suspend, and view fundraising activities |
| **Donee** | Browse activities, save favorites, view completed campaigns |
| **Platform Manager** | Manage fundraising categories, view daily/weekly/monthly reports |

## Running the Backend

Go to the backend folder:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend API documentation:

```
http://127.0.0.1:8000/docs
```

## Running the Frontend

Go to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the frontend development server:

```bash
npm run dev
```

Frontend server:

```
http://localhost:5173
```

## Environment Variables

Create a `.env` file inside the `backend/` folder:

```bash
DATABASE_URL=your_database_url
JWT_SECRET=your_secret_key
```

If `DATABASE_URL` is not set, the backend defaults to a local SQLite database (`test.db`).

## Seeding Demo Data

The backend automatically seeds demo data on startup. The following accounts are available:

```
User Admin:         admin@test.com      / admin123
Platform Manager:   manager@test.com    / manager123
Fundraiser:         fundraiser@test.com / fundraiser123
Donee:              donee@test.com      / donee123
```

## Running Tests

Tests use an isolated SQLite database and do not affect the shared/production database.

```bash
cd backend
pytest tests -v
```

The CI pipeline runs these tests automatically on every push or pull request to `main`.

## Notes

- Start the backend before using the frontend.
- If using Supabase, ensure `DATABASE_URL` is correctly set in `backend/.env`.
- If the database schema changes, existing Supabase tables may need to be dropped and recreated.
- The backend allows all CORS origins (`*`) — suitable for development only.
