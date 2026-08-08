from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.dependencies import get_db
from app.models.medication_model import Medication
from app.models.pet_model import Pet
from app.schemas.medicaiton_schema import (
    MedicationCreate,
    MedicationResponse,
    MedicationUpdate
)
from app.models.user_model import User
from app.models.pet_model import Pet
from app.utils.email_service import send_email
router = APIRouter(
    prefix="/medications",
    tags=["medications"]
)


@router.post("/", response_model=MedicationResponse)
async def create_medicaton(
    medication: MedicationCreate,
    db: Session = Depends(get_db)
):

    pet = db.query(Pet).filter(
        Pet.id == medication.pet_id
    ).first()

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    new_medication = Medication(
        pet_id=medication.pet_id,
        medicine_name=medication.medicine_name,
        dosage=medication.dosage,
        frequency=medication.frequency,
        start_date=medication.start_date,
        end_date=medication.end_date,
        reminder_time=medication.reminder_time,
        status=medication.status
    )

    db.add(new_medication)
    db.commit()
    db.refresh(new_medication)
    pet = db.query(Pet).filter(
    Pet.id == medication.pet_id
).first()

    if pet:

        owner = db.query(User).filter(
        User.id == pet.user_id
        ).first()

    if owner:

        subject = "Medication Scheduled - Pet Care Scheduler"

        body = f"""
Hello {owner.full_name},

A medication has been added for your pet.

Pet Name: {pet.pet_name}
Medicine: {new_medication.medicine_name}
Dosage: {new_medication.dosage}
Start Date: {new_medication.start_date}
End Date: {new_medication.end_date}

Please give the medication as prescribed.

Regards,
Pet Care Scheduler Team
"""

        await send_email(
            email=owner.email,
            subject=subject,
            body=body
        )
    return {
        "id": new_medication.id,
        "pet_id": pet.id,
        "pet_name": pet.pet_name,
        "medicine_name": new_medication.medicine_name,
        "dosage": new_medication.dosage,
        "frequency": new_medication.frequency,
        "start_date": new_medication.start_date,
        "end_date": new_medication.end_date,
        "reminder_time": new_medication.reminder_time,
        "status": new_medication.status
    }

@router.get("/", response_model=list[MedicationResponse])
def get_all_medication(db: Session = Depends(get_db)):

    medications = (
        db.query(Medication, Pet)
        .join(Pet, Medication.pet_id == Pet.id)
        .all()
    )

    result = []

    for medication, pet in medications:
        result.append({
            "id": medication.id,
            "pet_id": pet.id,
            "pet_name": pet.pet_name,
            "medicine_name": medication.medicine_name,
            "dosage": medication.dosage,
            "frequency": medication.frequency,
            "start_date": medication.start_date,
            "end_date": medication.end_date,
            "reminder_time": medication.reminder_time,
            "status": medication.status
        })

    return result
@router.get("/user/{user_id}", response_model=list[MedicationResponse])
def get_user_medications(
    user_id: int,
    db: Session = Depends(get_db)
):

    medications = (
        db.query(Medication, Pet)
        .join(Pet, Medication.pet_id == Pet.id)
        .filter(Pet.user_id == user_id)
        .all()
    )

    result = []

    for medication, pet in medications:
        result.append({
            "id": medication.id,
            "pet_id": pet.id,
            "pet_name": pet.pet_name,
            "medicine_name": medication.medicine_name,
            "dosage": medication.dosage,
            "frequency": medication.frequency,
            "start_date": medication.start_date,
            "end_date": medication.end_date,
            "reminder_time": medication.reminder_time,
            "status": medication.status
        })

    return result

@router.get("/today", response_model=list[MedicationResponse])
def get_todays_medications(db: Session = Depends(get_db)):

    today = date.today()

    medications = (
        db.query(Medication, Pet)
        .join(Pet, Medication.pet_id == Pet.id)
        .filter(
            Medication.start_date <= today,
            Medication.end_date >= today,
            Medication.status == "Active"
        )
        .all()
    )

    result = []

    for medication, pet in medications:
        result.append({
            "id": medication.id,
            "pet_id": pet.id,
            "pet_name": pet.pet_name,
            "medicine_name": medication.medicine_name,
            "dosage": medication.dosage,
            "frequency": medication.frequency,
            "start_date": medication.start_date,
            "end_date": medication.end_date,
            "reminder_time": medication.reminder_time,
            "status": medication.status
        })

    return result


@router.get("/{medication_id}", response_model=MedicationResponse)
def get_medication_by_id(
    medication_id: int,
    db: Session = Depends(get_db)
):

    medication = (
        db.query(Medication, Pet)
        .join(Pet, Medication.pet_id == Pet.id)
        .filter(Medication.id == medication_id)
        .first()
    )

    if medication is None:
        raise HTTPException(
            status_code=404,
            detail="Medication not found"
        )

    medication_obj, pet = medication

    return {
        "id": medication_obj.id,
        "pet_id": pet.id,
        "pet_name": pet.pet_name,
        "medicine_name": medication_obj.medicine_name,
        "dosage": medication_obj.dosage,
        "frequency": medication_obj.frequency,
        "start_date": medication_obj.start_date,
        "end_date": medication_obj.end_date,
        "reminder_time": medication_obj.reminder_time,
        "status": medication_obj.status
    }
@router.get("/send-reminders")
async def send_medication_reminders(
    db: Session = Depends(get_db)
):

    today = date.today()

    medications = db.query(Medication).filter(
        Medication.end_date >= today
    ).all()

    count = 0

    for medication in medications:

        pet = db.query(Pet).filter(
            Pet.id == medication.pet_id
        ).first()

        if not pet:
            continue

        owner = db.query(User).filter(
            User.id == pet.user_id
        ).first()

        if not owner:
            continue

        subject = "Medication Reminder - Pet Care Scheduler"

        body = f"""
Hello {owner.full_name},

Medication reminder for your pet.

Pet Name: {pet.pet_name}
Medicine: {medication.medicine_name}
Dosage: {medication.dosage}
End Date: {medication.end_date}

Please do not miss today's dose.

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
        "message": f"{count} medication reminder emails sent"
    }

@router.put("/{medication_id}", response_model=MedicationResponse)
def update_medication(
    medication_id: int,
    updated_medication: MedicationUpdate,
    db: Session = Depends(get_db)
):

    medication = db.query(Medication).filter(
        Medication.id == medication_id
    ).first()

    if medication is None:
        raise HTTPException(
            status_code=404,
            detail="Medication not found"
        )

    medication.pet_id = updated_medication.pet_id
    medication.medicine_name = updated_medication.medicine_name
    medication.dosage = updated_medication.dosage
    medication.frequency = updated_medication.frequency
    medication.start_date = updated_medication.start_date
    medication.end_date = updated_medication.end_date
    medication.reminder_time = updated_medication.reminder_time
    medication.status = updated_medication.status

    db.commit()
    db.refresh(medication)

    pet = db.query(Pet).filter(
        Pet.id == medication.pet_id
    ).first()

    return {
        "id": medication.id,
        "pet_id": pet.id,
        "pet_name": pet.pet_name,
        "medicine_name": medication.medicine_name,
        "dosage": medication.dosage,
        "frequency": medication.frequency,
        "start_date": medication.start_date,
        "end_date": medication.end_date,
        "reminder_time": medication.reminder_time,
        "status": medication.status
    }


@router.delete("/{medication_id}")
def delete_medication(
    medication_id: int,
    db: Session = Depends(get_db)
):

    medication = db.query(Medication).filter(
        Medication.id == medication_id
    ).first()

    if medication is None:
        raise HTTPException(
            status_code=404,
            detail="Medication not found"
        )

    db.delete(medication)
    db.commit()

    return {
        "message": "Medication deleted successfully"
    }