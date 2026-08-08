from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.pet_model import Pet
from app.schemas.pet_schema import PetCreate,PetResponse,PetUpdate
from app.models.vaccinaton_model import Vaccination
from app.models.medication_model import Medication
from app.models.appointment_model import Appointment
from app.schemas.history_schema import PetHistoryResponse

router =APIRouter(
    prefix="/pets",
    tags=["Pets"]
)

@router.post("/",response_model=PetResponse)
def create_pet(pet:PetCreate,db:Session=Depends(get_db)):
    new_pet=Pet(
        user_id=pet.user_id,
        pet_name=pet.pet_name,
        species=pet.species,
        breed=pet.breed,
        gender=pet.gender,
        age=pet.age,
        weight=pet.weight,
        photo_url=pet.photo_url
    )

    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return new_pet

@router.get("/",response_model=list[PetResponse])
def get_all_pets(db:Session=Depends(get_db)):
    pets=db.query(Pet).all()
    return pets
@router.get("/user/{user_id}",
            response_model=list[PetResponse])
def get_user_pets(
    user_id:int,
    db:Session=Depends(get_db)
):

    pets = db.query(Pet).filter(
        Pet.user_id == user_id
    ).all()

    return pets

@router.get("/{pet_id}/history",response_model=PetHistoryResponse)
def get_pet_history(pet_id : int,db:Session=Depends(get_db)):
    pet=db.query(Pet).filter(Pet.id==pet_id).first()

    if pet is None :
        raise HTTPException(
            status_code=404,
            detail="pet not found"
        )

    vaccinations=db.query(Vaccination).filter(Vaccination.pet_id==pet_id).all()

    medications=db.query(Medication).filter(Medication.pet_id==pet_id).all()

    appointments=db.query(Appointment).filter(Appointment.pet_id==pet_id).all()

    return PetHistoryResponse(
        pet=pet,
        vaccinations=vaccinations,
        medications =medications,
        appointments=appointments
    )
@router.get("/profile/{pet_id}")
def get_pet_profile(
    pet_id: int,
    db: Session = Depends(get_db)
):

    pet = db.query(Pet).filter(
        Pet.id == pet_id
    ).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    vaccination_count = len(
        pet.vaccinations
    )

    medication_count = len(
        pet.medications
    )

    appointment_count = len(
        pet.appointments
    )
    health_score = 50

    if vaccination_count > 0:
        health_score += 20

    if medication_count > 0:
        health_score += 15

    if appointment_count > 0:
        health_score += 15

    if health_score > 100:
        health_score = 100
    if health_score >= 90:
        health_status = "Excellent 🟢"

    elif health_score >= 75:
        health_status = "Good 🟢"

    elif health_score >= 60:
        health_status = "Average 🟡"

    else:
        health_status = "Needs Attention 🔴"
    return {
    "id": pet.id,
    "pet_name": pet.pet_name,
    "species": pet.species,
    "breed": pet.breed,
    "gender": pet.gender,
    "age": pet.age,
    "weight": pet.weight,
    "photo_url": pet.photo_url,
    "vaccinations": vaccination_count,
    "medications": medication_count,
    "appointments": appointment_count,
    "health_score": health_score,
    "health_status": health_status
    }
@router.get("/{pet_id}",response_model=PetResponse)
def get_pet_by_id(pet_id:int,db:Session=Depends(get_db)):
    pet=db.query(Pet).filter(Pet.id==pet_id).first()

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="no pet found "
        )

    return pet 

@router.put("/{pet_id}",response_model=PetResponse)
def update_pet(pet_id:int,updated_pet:PetUpdate,db:Session=Depends(get_db)):
    pet=db.query(Pet).filter(Pet.id==pet_id).first()

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="pet not found"
        )
    pet.user_id=updated_pet.user_id
    pet.pet_name=updated_pet.pet_name
    pet.species=updated_pet.species
    pet.breed=updated_pet.breed
    pet.gender=updated_pet.gender
    pet.age=updated_pet.age
    pet.weight=updated_pet.weight
    pet.photo_url = updated_pet.photo_url
    db.commit()
    db.refresh(pet)

    return pet

@router.delete("/{pet_id}")
def delete_pet(pet_id : int,db:Session=Depends(get_db)):
    pet =db.query(Pet).filter(Pet.id==pet_id).first()

    if pet is None : 
        raise HTTPException(
            status_code=404,
            detail="pet not found "
        )

    db.delete(pet)
    db.commit()

    return{
        "message":"pet deleted successfully "
    }
