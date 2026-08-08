from sqlalchemy import Integer,String,Column,Float,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Pet(Base):
    __tablename__="pets"

    id =Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    pet_name=Column(String)
    species=Column(String)
    breed=Column(String)
    gender=Column(String)
    age=Column(Integer)
    weight=Column(Float)
    photo_url = Column(String, nullable=True)
    owner =relationship(
        "User",
        back_populates="pets"
    )

    vaccinations = relationship(
    "Vaccination",
    back_populates="pet",
    cascade="all,delete"
    )

    medications = relationship(
    "Medication",
    back_populates="pet",
    cascade="all, delete"
    )

    appointments = relationship(
    "Appointment",
    back_populates="pet",
    cascade="all, delete"
    )

    



