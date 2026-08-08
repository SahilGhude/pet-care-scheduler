from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import date,timedelta

from app.schemas.appointment_schema import (
    AppointmentCreate,
    AppointmentResponse,
    ApointmentUpdate
)
from app.models.appointment_model import Appointment
from app.models.pet_model import Pet
from app.dependencies import get_db
from app.models.pet_model import Pet
from app.models.user_model import User
from app.utils.email_service import send_email

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):

    pet = db.query(Pet).filter(
        Pet.id == appointment.pet_id
    ).first()

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    new_appointment = Appointment(
        pet_id=appointment.pet_id,
        doctor_name=appointment.doctor_name,
        clinic_name=appointment.clinic_name,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        purpose=appointment.purpose,
        status=appointment.status,
        notes=appointment.notes
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    owner = db.query(User).filter(
    User.id == pet.user_id
        ).first()

    if owner:

        subject = "Appointment Confirmed - Pet Care Scheduler"

        body = f"""
        Hello {owner.full_name},

        Your appointment has been successfully scheduled.

        Pet Name: {pet.pet_name}
        Doctor: {new_appointment.doctor_name}
        Clinic: {new_appointment.clinic_name}
        Date: {new_appointment.appointment_date}
        Time: {new_appointment.appointment_time}
        Purpose: {new_appointment.purpose}

        Thank you for using Pet Care Scheduler.

        Regards,
        Pet Care Scheduler Team
        """

        try:
             await send_email(
            email=owner.email,
            subject=subject,
            body=body
                )
        except Exception as e:
            print("Email Error:", e)

    return {
        "id": new_appointment.id,
        "pet_id": pet.id,
        "pet_name": pet.pet_name,
        "doctor_name": new_appointment.doctor_name,
        "clinic_name": new_appointment.clinic_name,
        "appointment_date": new_appointment.appointment_date,
        "appointment_time": new_appointment.appointment_time,
        "purpose": new_appointment.purpose,
        "status": new_appointment.status,
        "notes": new_appointment.notes
    }


@router.get("/", response_model=list[AppointmentResponse])
def get_all_appointment(db: Session = Depends(get_db)):

    appointments = (
        db.query(Appointment, Pet)
        .join(Pet, Appointment.pet_id == Pet.id)
        .all()
    )

    result = []

    for appointment, pet in appointments:
        result.append({
            "id": appointment.id,
            "pet_id": pet.id,
            "pet_name": pet.pet_name,
            "doctor_name": appointment.doctor_name,
            "clinic_name": appointment.clinic_name,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
            "purpose": appointment.purpose,
            "status": appointment.status,
            "notes": appointment.notes
        })

    return result
@router.get("/user/{user_id}", response_model=list[AppointmentResponse])
def get_user_appointments(
    user_id: int,
    db: Session = Depends(get_db)
):

    appointments = (
        db.query(Appointment, Pet)
        .join(Pet, Appointment.pet_id == Pet.id)
        .filter(Pet.user_id == user_id)
        .all()
    )

    result = []

    for appointment, pet in appointments:
        result.append({
            "id": appointment.id,
            "pet_id": pet.id,
            "pet_name": pet.pet_name,
            "doctor_name": appointment.doctor_name,
            "clinic_name": appointment.clinic_name,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
            "purpose": appointment.purpose,
            "status": appointment.status,
            "notes": appointment.notes
        })

    return result

@router.get("/today", response_model=list[AppointmentResponse])
def get_todays_appointment(db: Session = Depends(get_db)):

    today = date.today()

    appointments = (
        db.query(Appointment, Pet)
        .join(Pet, Appointment.pet_id == Pet.id)
        .filter(Appointment.appointment_date == today)
        .all()
    )

    result = []

    for appointment, pet in appointments:
        result.append({
            "id": appointment.id,
            "pet_id": pet.id,
            "pet_name": pet.pet_name,
            "doctor_name": appointment.doctor_name,
            "clinic_name": appointment.clinic_name,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
            "purpose": appointment.purpose,
            "status": appointment.status,
            "notes": appointment.notes
        })

    return result

@router.get("/send-reminders")
async def send_appointment_reminders(
    db: Session = Depends(get_db)
):

    today = date.today()

    reminder_date = today + timedelta(days=1)

    appointments = db.query(Appointment).filter(
        Appointment.appointment_date == reminder_date
    ).all()

    count = 0

    for appointment in appointments:

        pet = db.query(Pet).filter(
            Pet.id == appointment.pet_id
        ).first()

        if not pet:
            continue

        owner = db.query(User).filter(
            User.id == pet.user_id
        ).first()

        if not owner:
            continue

        subject = "Appointment Reminder - Pet Care Scheduler"

        body = f"""
Hello {owner.full_name},

Reminder: Your pet appointment is tomorrow.

Pet Name: {pet.pet_name}
Doctor: {appointment.doctor_name}
Clinic: {appointment.clinic_name}
Date: {appointment.appointment_date}
Time: {appointment.appointment_time}

Please visit the clinic on time.

Regards,
Pet Care Scheduler Team
"""

        await send_email(
            email=owner.email,
            subject=subject,
            body=body
        )

        count += 1

    return {
        "message": f"{count} appointment reminder emails sent"
    }
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment_by_id(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = (
        db.query(Appointment, Pet)
        .join(Pet, Appointment.pet_id == Pet.id)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment_obj, pet = appointment

    return {
        "id": appointment_obj.id,
        "pet_id": pet.id,
        "pet_name": pet.pet_name,
        "doctor_name": appointment_obj.doctor_name,
        "clinic_name": appointment_obj.clinic_name,
        "appointment_date": appointment_obj.appointment_date,
        "appointment_time": appointment_obj.appointment_time,
        "purpose": appointment_obj.purpose,
        "status": appointment_obj.status,
        "notes": appointment_obj.notes
    }


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment_update: ApointmentUpdate,
    db: Session = Depends(get_db)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    pet = db.query(Pet).filter(
        Pet.id == appointment_update.pet_id
    ).first()

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    appointment.pet_id = appointment_update.pet_id
    appointment.doctor_name = appointment_update.doctor_name
    appointment.clinic_name = appointment_update.clinic_name
    appointment.appointment_date = appointment_update.appointment_date
    appointment.appointment_time = appointment_update.appointment_time
    appointment.purpose = appointment_update.purpose
    appointment.status = appointment_update.status
    appointment.notes = appointment_update.notes

    db.commit()
    db.refresh(appointment)

    return {
        "id": appointment.id,
        "pet_id": pet.id,
        "pet_name": pet.pet_name,
        "doctor_name": appointment.doctor_name,
        "clinic_name": appointment.clinic_name,
        "appointment_date": appointment.appointment_date,
        "appointment_time": appointment.appointment_time,
        "purpose": appointment.purpose,
        "status": appointment.status,
        "notes": appointment.notes
    }


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }