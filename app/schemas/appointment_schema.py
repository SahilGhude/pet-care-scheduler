from pydantic import BaseModel, ConfigDict
from datetime import date,time 

class AppointmentCreate(BaseModel):
    pet_id:int
    doctor_name :str
    clinic_name:str
    appointment_date:date
    appointment_time:time
    purpose:str
    status:str
    notes :str

class AppointmentResponse(BaseModel):
    id: int
    pet_id: int
    pet_name: str
    doctor_name: str
    clinic_name: str
    appointment_date: date
    appointment_time: time
    purpose: str
    status: str
    notes: str

    class Config:
        from_attributes = True
        
class ApointmentUpdate(BaseModel):
    pet_id:int
    doctor_name :str
    clinic_name:str
    appointment_date:date
    appointment_time:time
    purpose:str
    status:str
    notes :str


class AppointmentHistoryResponse(BaseModel):
    id: int
    appointment_date: date
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )
