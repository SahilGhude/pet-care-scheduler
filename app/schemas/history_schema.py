from pydantic import BaseModel

from app.schemas.pet_schema import PetResponse
from app.schemas.vaccinaton_schema import VaccinationHistoryResponse
from app.schemas.medicaiton_schema import MedicationHistoryResponse
from app.schemas.appointment_schema import AppointmentHistoryResponse


class PetHistoryResponse(BaseModel):
    pet: PetResponse
    vaccinations: list[VaccinationHistoryResponse]
    medications: list[MedicationHistoryResponse]
    appointments: list[AppointmentHistoryResponse]