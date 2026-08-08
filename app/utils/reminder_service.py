from datetime import date, timedelta

from app.database import SessionLocal
from app.models.vaccinaton_model import Vaccination
from app.models.pet_model import Pet
from app.models.user_model import User
from app.utils.email_service import send_email
import asyncio
from app.models.medication_model import Medication
from app.models.appointment_model import Appointment


def send_vaccination_reminders():

    db = SessionLocal()

    try:

        today = date.today()

        reminder_date = today + timedelta(days=1)

        print("Today:", today)
        print("Checking reminders for:", reminder_date)

        vaccinations = db.query(Vaccination).filter(
            Vaccination.next_due_date == reminder_date
        ).all()

        print("Vaccinations Found:", len(vaccinations))

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

Reminder: Your pet vaccination is due tomorrow.

Pet Name: {pet.pet_name}
Vaccine: {vaccination.vaccine_name}
Due Date: {vaccination.next_due_date}

Please schedule the vaccination on time.

Regards,
Pet Care Scheduler Team
"""

            print("Sending email to:", owner.email)

            # IMPORTANT:
            # APScheduler cannot directly await async functions
            # so for now comment this line

            asyncio.run(
                send_email(
                    email=owner.email,
                    subject=subject,
                    body=body
            )
)

    finally:

        db.close()

def send_medication_reminders():

    db = SessionLocal()

    try:

        today = date.today()
        print("Checking medication reminders for:", today)
        medications = db.query(Medication).filter(
            Medication.start_date <= today,
            Medication.end_date >= today
        ).all()
        print("Medications Found:", len(medications))

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

This is your daily medication reminder.

Pet Name: {pet.pet_name}
Medicine: {medication.medicine_name}

Start Date: {medication.start_date}
End Date: {medication.end_date}

Please give the medication today as prescribed.

Regards,
Pet Care Scheduler Team
"""

            print("Sending medication email to:", owner.email)

            asyncio.run(
                send_email(
                    email=owner.email,
                    subject=subject,
                    body=body
                )
            )

    finally:

        db.close()

def send_appointment_reminders():

    db = SessionLocal()

    try:

        today = date.today()

        reminder_date = today + timedelta(days=1)

        print("Checking appointment reminders for:", reminder_date)

        appointments = db.query(Appointment).filter(
            Appointment.appointment_date == reminder_date
        ).all()

        print("Appointments Found:", len(appointments))

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

Reminder: Your pet has an appointment tomorrow.

Pet Name: {pet.pet_name}
Doctor: {appointment.doctor_name}
Clinic: {appointment.clinic_name}
Date: {appointment.appointment_date}
Time: {appointment.appointment_time}
Purpose: {appointment.purpose}

Please make sure to attend the appointment.

Regards,
Pet Care Scheduler Team
"""

            asyncio.run(
                send_email(
                    email=owner.email,
                    subject=subject,
                    body=body
                )
            )

    finally:

        db.close()