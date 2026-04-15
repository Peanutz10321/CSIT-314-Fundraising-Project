from contextlib import contextmanager
from app.database import SessionLocal


class BaseEntity:
    @contextmanager
    def session_scope(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
