from pydantic import BaseModel, ConfigDict
from datetime import date

class VaccinationCreate(BaseModel):
    pet_id :int
    vaccine_name:str
    vaccination_date:date
    next_due_date:date
    status:str
    notes:str

class VaccinationResponse(BaseModel):
    id :int
    pet_id:int
    pet_name: str 
    vaccine_name:str
    vaccination_date:date
    next_due_date:date
    status:str 
    notes: str 

    class config:
        from_attributes =True

class VaccinationUpdate(BaseModel):
    pet_id:int
    vaccine_name:str
    vaccination_date:date
    next_due_date:date
    status:str 
    notes:str

class VaccinationHistoryResponse(BaseModel):
    id: int
    vaccine_name: str
    vaccination_date: date
    next_due_date: date
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )