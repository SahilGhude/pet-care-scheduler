from datetime import date 
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from app.dependencies import get_db
from app.models.user_model import User
from app.models.pet_model import Pet
from app.models.medication_model import Medication
from app.models.vaccinaton_model import Vaccination
from app.models.appointment_model import Appointment
from app.schemas.dashboard_schema import DashboardResponse

router =APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/",response_model=DashboardResponse)
def get_dashboard(db:Session=Depends(get_db)):
    total_users=db.query(User).count()
    total_pets=db.query(Pet).count()
    total_vaccinations=db.query(Vaccination).count()

    active_medications=db.query(Medication).filter(Medication.status=="Active").count()
    today_appointments=db.query(Appointment).filter(Appointment.appointment_date==date.today).count()

    return DashboardResponse(
        total_users=total_users,
        total_pets=total_pets,
        total_vaccimations=total_vaccinations,
        active_medications=active_medications,
        today_appointments=today_appointments
    )