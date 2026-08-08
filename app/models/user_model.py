from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True)
    password = Column(String, nullable=False)

    pets = relationship(
        "Pet",
        back_populates="owner",
        cascade="all, delete"
    )