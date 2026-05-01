# Fundraising Platform

This project is an online fundraising platform developed for the **CSIT314 Software Development Methodologies** group project.


## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, Python
- **Frontend:** React, Vite, CSS
- **Testing:** Pytest
- **CI:** GitHub Actions

## Project Structure
```bash
backend/
  app/
  tests/
frontend/
  src/
    api/
    components/
    pages/
  package.json
  vite.config.js
```

## Running the Backend
- cd backend
- uvicorn app.main:app --reload

### Backend docs
http://127.0.0.1:8000/docs

## Running the frontend
- cd frontend
- npm install
- npm run dev

### Frontend Server(usually)
http://localhost:5173
