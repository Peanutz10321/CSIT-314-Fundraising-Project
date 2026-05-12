# Fundraising Platform

This project is an online fundraising platform developed for the **CSIT314 Software Development Methodologies** group project.


## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, Python
- **Frontend:** React, Vite, CSS
- **Database:** SQLite for local automated testing, Supabase PostgreSQL for shared/demo database
- **Testing:** Pytest
- **CI:** GitHub Actions

## Project Structure
```bash
backend/
  app/
    controllers/
    entities/
    routes/
    schemas/
    middleware/
    seeds/
    main.py
  tests/
  requirements.txt

frontend/
  src/
    api/
    components/
    pages/
  package.json
  vite.config.js
```

## Running the Backend

Go to the backend folder:

```bash
cd backend
```

Create and activate a virtual environment if needed:

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

```text
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

```text
http://localhost:5173
```
## Environment variables
Create a .env file in the backend if using a custom database or secret key.

Example 
```bash
DATABASE_URL=your_database_url
JWT_SECRET=your_secret_key
```

## Seeding Demo Data

The project includes seed scripts for demo and testing data.

Example demo accounts:

```text
User Admin: admin@test.com / admin123
Platform Manager: manager@test.com / manager123
Fundraiser: fundraiser@test.com / fundraiser123
Donee: donee@test.com / donee123
```

## Notes

- Start the backend before using the frontend.
- Make sure database tables are created before running the full system.
- If using Supabase, ensure `DATABASE_URL` is correctly configured.
- If the database schema changes, old Supabase tables may need to be dropped/recreated or migrated.