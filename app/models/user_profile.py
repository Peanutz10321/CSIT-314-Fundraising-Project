from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Enum
import enum

Base = declarative_base()

class Role(str, enum.Enum):
    USER_ADMIN = "USER_ADMIN"
    PLATFORM_MANAGER = "PLATFORM_MANAGER"
    FUNDRAISER = "FUNDRAISER"
    DONEE = "DONEE"

class Status(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    status = Column(Enum(Status), default=Status.ACTIVE)

    def get_password(self): 
        pass

    def set_password(self, p): 
        pass

    def suspend(self): 
        pass

    def to_dict(self): 
        return {}
    
    def get_dashboard_info(self): 
        return {}

class Fundraiser(UserProfile): 
    pass

class Donee(UserProfile): 
    pass

class PlatformManager(UserProfile): 
    pass

class UserAdmin(UserProfile): 
    pass

def create_user_by_role(name, email, password, role, description=None):
    pass