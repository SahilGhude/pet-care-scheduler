from fastapi import FastAPI
from app.config import settings
from app.database import Base,engine
from app.models.user_model import User
from app.models.pet_model import Pet
from app.models.vaccinaton_model import Vaccination
from app.models.medication_model import Medication
from app.models.appointment_model import Appointment
from app.routers.user_router import router as user_router
from app.routers.pet_router import router as pet_router 
from app.routers.vaccination_router import router as vaccination_router
from app.routers.mediacion_router import router as medication_router 
from app.routers.appointment_router import router as appointment_router 
from app.routers.dashboard_router import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware
from app.routers.email_router import router as email_router 
from app.utils.scheduler import scheduler
from apscheduler.triggers.cron import CronTrigger
from app.utils.reminder_service import (
    send_vaccination_reminders,
    send_medication_reminders,
     send_appointment_reminders
)



app=FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pet-care-scheduler-2026.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(pet_router)
app.include_router(vaccination_router)
app.include_router(medication_router)
app.include_router(appointment_router)
app.include_router(dashboard_router)
app.include_router(email_router)
@app.get("/")
def home():
    return {
        "message":"hii , welcome to pet care scheduler API"
    }
@app.on_event("startup")
def start_scheduler():

    scheduler.add_job(
        send_vaccination_reminders,
        CronTrigger(hour=9, minute=0),
        id="vaccination_reminder",
        replace_existing=True
    )

    scheduler.add_job(
        send_medication_reminders,
        CronTrigger(hour=9, minute=0),
        id="medication_reminder",
        replace_existing=True
    )
    scheduler.add_job(
    send_appointment_reminders,
    CronTrigger(hour=9, minute=0),
    id="appointment_reminder",
    replace_existing=True
    )

    scheduler.start()