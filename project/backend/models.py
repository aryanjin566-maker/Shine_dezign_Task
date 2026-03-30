from sqlalchemy import Column, Integer, String, Text
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    user_id = Column(String(50), unique=True)
    image_path = Column(Text)