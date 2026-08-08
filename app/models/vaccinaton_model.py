from sqlalchemy import String, Integer, Date, ForeignKey, Column
from app.database import Base
from sqlalchemy.orm import relationship

class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    vaccine_name = Column(String)
    vaccination_date = Column(Date)
    next_due_date = Column(Date)
    status = Column(String)
    notes = Column(String)

    pet = relationship(
        "Pet",
        back_populates="vaccinations"
    )