from sqlalchemy import Column,Integer,String,Date,Time,ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Appointment(Base):
    __tablename__="appointments"

    id =Column(Integer,primary_key=True,index=True)
    pet_id =Column(Integer,ForeignKey("pets.id"))
    doctor_name=Column(String)
    clinic_name=Column(String)
    appointment_date=Column(Date)
    appointment_time=Column(Time)
    purpose=Column(String)
    status=Column(String)
    notes=Column(String)

    pet =relationship(
        "Pet",
        back_populates="appointments"
    )
