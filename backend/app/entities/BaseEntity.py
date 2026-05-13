from app.database import get_session


class BaseEntity:
    @staticmethod
    def open_session():
        return get_session()
