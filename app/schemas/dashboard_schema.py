from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total_users:int
    total_pets:int 
    total_vaccinations:int
    active_medicines:int 
    today_appointments:int 


    
