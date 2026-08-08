from sqlalchemy import String,Integer,Date,ForeignKey,Time,Column
from app.database import Base
from sqlalchemy.orm import relationship

class Medication(Base):
    __tablename__="medications"

    id =Column(Integer,primary_key=True,index=True)
    pet_id =Column(Integer,ForeignKey("pets.id"))
    medicine_name=Column(String)
    dosage =Column(String )
    frequency=Column(String )
    start_date=Column(Date)
    end_date=Column(Date)
    reminder_time=Column(Time)
    status=Column(String )

    pet = relationship(
    "Pet",
    back_populates="medications"
    )
