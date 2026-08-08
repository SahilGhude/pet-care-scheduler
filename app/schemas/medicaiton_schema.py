from pydantic import BaseModel, ConfigDict
from datetime import date,time 

class MedicationCreate(BaseModel):
    pet_id:int 
    medicine_name :str 
    dosage:str 
    frequency:str 
    start_date :date 
    end_date:date 
    reminder_time :time 
    status :str 

class MedicationResponse(BaseModel):
    id :int 
    pet_id:int
    pet_name: str 
    medicine_name :str 
    dosage:str 
    frequency:str 
    start_date :date 
    end_date:date 
    reminder_time :time 
    status :str 

    class config:
        from_attributes=True

class MedicationUpdate(BaseModel):
    pet_id:int 
    medicine_name :str 
    dosage:str 
    frequency:str 
    start_date :date 
    end_date:date 
    reminder_time :time 
    status :str 



class MedicationHistoryResponse(BaseModel):
    id: int
    medicine_name: str
    dosage: str
    frequency: str
    start_date: date
    end_date: date
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )