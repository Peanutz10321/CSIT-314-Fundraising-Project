from fastapi import FastAPI
from app.routes import user, auth
from app.database import create_tables
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fundraising API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()

app.include_router(auth.router)        
app.include_router(user.router)
