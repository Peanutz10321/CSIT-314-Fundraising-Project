from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app.routes import user_profile, auth
from app.seeds.seed_user_profiles import seed_user_profiles
from app.seeds.seed_test_admin import seed_test_admin
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fundraising API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_startup_seeds():
    db: Session = SessionLocal()
    try:
        seed_user_profiles(db)
        seed_test_admin(db)
    finally:
        db.close()


run_startup_seeds()

app.include_router(user_profile.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Fundraising API is running"}