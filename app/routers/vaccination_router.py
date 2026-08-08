from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.vaccinaton_model import Vaccination
from app.schemas.vaccinaton_schema import VaccinationCreate,VaccinationResponse,VaccinationUpdate
from datetime import date,timedelta
from app.models.pet_model import Pet
from app.models.user_model import User
from app.utils.email_service import send_email


router =APIRouter(
    prefix="/vaccinations",
    tags=["vaccinations"]
)

@router.post("/", response_model=VaccinationResponse)
async def create_vaccination(
    vaccination: VaccinationCreate,
    db: Session = Depends(get_db)
):
  new_vaccine=Vaccination(
    pet_id=vaccination.pet_id,
    vaccine_name=vaccination.vaccine_name,
    vaccination_date=vaccination.vaccination_date,
    next_due_date=vaccination.next_due_date,
    status=vaccination.status,
    notes=vaccination.notes
  )

  db.add(new_vaccine)
  db.commit()
  db.refresh(new_vaccine)
  pet = db.query(Pet).filter(
  Pet.id == vaccination.pet_id
    ).first()

  if pet:

        owner = db.query(User).filter(
        User.id == pet.user_id
             ).first()

  if owner:

        subject = "Vaccination Scheduled - Pet Care Scheduler"

        body = f"""
        Hello {owner.full_name},

        A vaccination has been scheduled for your pet.

        Pet Name: {pet.pet_name}
        Vaccine: {new_vaccine.vaccine_name}
        Vaccination Date: {new_vaccine.vaccination_date}
        Next Due Date: {new_vaccine.next_due_date}
        Status: {new_vaccine.status}

        Thank you for using Pet Care Scheduler.

        Regards,
        Pet Care Scheduler Team
        """

        await send_email(
            email=owner.email,
            subject=subject,
            body=body
        )
  return {
    "id": new_vaccine.id,
    "pet_id": pet.id,
    "pet_name": pet.pet_name,
    "vaccine_name": new_vaccine.vaccine_name,
    "vaccination_date": new_vaccine.vaccination_date,
    "next_due_date": new_vaccine.next_due_date,
    "status": new_vaccine.status,
    "notes": new_vaccine.notes
    }
@router.get("/", response_model=list[VaccinationResponse])
def get_all_vaccinations(db: Session = Depends(get_db)):

    vaccinations = (
        db.query(Vaccination, Pet)
        .join(Pet, Vaccination.pet_id == Pet.id)
        .all()
    )

    result = []

    for vaccination, pet in vaccinations:
        result.append({
            "id": vaccination.id,
            "pet_id": pet.id,
            "pet_name": pet.pet_name,
            "vaccine_name": vaccination.vaccine_name,
            "vaccination_date": vaccination.vaccination_date,
            "next_due_date": vaccination.next_due_date,
            "status": vaccination.status,
            "notes": vaccination.notes
        })

    return result
@router.get(
    "/user/{user_id}",
    response_model=list[VaccinationResponse]
)
def get_user_vaccinations(
    user_id: int,
    db: Session = Depends(get_db)
):

    vaccinations = (
        db.query(Vaccination, Pet)
        .join(Pet, Vaccination.pet_id == Pet.id)
        .filter(Pet.user_id == user_id)
        .all()
    )

    result = []

    for vaccination, pet in vaccinations:

        result.append({
            "id": vaccination.id,
            "pet_id": pet.id,
            "pet_name": pet.pet_name,
            "vaccine_name": vaccination.vaccine_name,
            "vaccination_date": vaccination.vaccination_date,
            "next_due_date": vaccination.next_due_date,
            "status": vaccination.status,
            "notes": vaccination.notes
        })

    return result




@router.put("/{vaccination_id}", response_model=VaccinationResponse)
def update_vaccination(
    vaccination_id: int,
    updated: VaccinationUpdate,
    db: Session = Depends(get_db)
):

    updated_vaccination = db.query(Vaccination).filter(
        Vaccination.id == vaccination_id
    ).first()

    if updated_vaccination is None:
        raise HTTPException(
            status_code=404,
            detail="Vaccination not found"
        )

    updated_vaccination.pet_id = updated.pet_id
    updated_vaccination.vaccine_name = updated.vaccine_name
    updated_vaccination.vaccination_date = updated.vaccination_date
    updated_vaccination.next_due_date = updated.next_due_date
    updated_vaccination.status = updated.status
    updated_vaccination.notes = updated.notes

    db.commit()
    db.refresh(updated_vaccination)

    pet = db.query(Pet).filter(
      Pet.id == updated_vaccination.pet_id
    ).first()

    return {
      "id": updated_vaccination.id,
      "pet_id": pet.id,
      "pet_name": pet.pet_name,
      "vaccine_name": updated_vaccination.vaccine_name,
      "vaccination_date": updated_vaccination.vaccination_date,
      "next_due_date": updated_vaccination.next_due_date,
      "status": updated_vaccination.status,
      "notes": updated_vaccination.notes
    }

@router.delete("/{vaccination_id}")
def delete_vaccination(vaccination_id:int ,db:Session=Depends(get_db)):
  vaccination=db.query(Vaccination).filter(Vaccination.id==vaccination_id).first()

  if vaccination is None :
    raise HTTPException(
      status_code=404,
      detail="id not found"
    )

  db.delete(vaccination)
  db.commit()
  return {

    "message ":"vaccinaiton deleted successfully "
   }
@router.get("/send-reminders")
async def send_vaccination_reminders(
    db: Session = Depends(get_db)
):

    today = date.today()

    reminder_date = today + timedelta(days=1)

    vaccinations = db.query(Vaccination).filter(
    Vaccination.next_due_date == reminder_date
    ).all()
    count = 0

    for vaccination in vaccinations:

        pet = db.query(Pet).filter(
            Pet.id == vaccination.pet_id
        ).first()

        if not pet:
            continue
        owner = db.query(User).filter(
            User.id == pet.user_id
        ).first()

        if not owner:
            continue

        subject = "Vaccination Reminder - Pet Care Scheduler"

        body = f"""
        Hello {owner.full_name},

        Reminder: Your pet vaccination is due soon.

        pet Name: {pet.pet_name}
        Vaccine: {vaccination.vaccine_name}
        Due Date: {vaccination.next_due_date}

        Please schedule the vaccination on time.

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
        "message": f"{count} reminder emails sent"
    }
@router.get("/{vaccination_id}", response_model=VaccinationResponse)
def get_vaccination_by_id(vaccination_id: int, db: Session = Depends(get_db)):

    vaccination = (
        db.query(Vaccination, Pet)
        .join(Pet, Vaccination.pet_id == Pet.id)
        .filter(Vaccination.id == vaccination_id)
        .first()
    )

    if vaccination is None:
        raise HTTPException(
            status_code=404,
            detail="Vaccination not found"
        )

    vaccination_obj, pet = vaccination

    return {
        "id": vaccination_obj.id,
        "pet_id": pet.id,
        "pet_name": pet.pet_name,
        "vaccine_name": vaccination_obj.vaccine_name,
        "vaccination_date": vaccination_obj.vaccination_date,
        "next_due_date": vaccination_obj.next_due_date,
        "status": vaccination_obj.status,
        "notes": vaccination_obj.notes
    }
