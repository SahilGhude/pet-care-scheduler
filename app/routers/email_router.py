from fastapi import APIRouter
from app.utils.email_service import send_email

router = APIRouter(
    prefix="/email",
    tags=["Email"]
)

@router.get("/test")
async def test_email():

    await send_email(
        email="sahilghude1145@gmail.com",
        subject="Pet Care Scheduler Test",
        body="Congratulations! Your Pet Care Scheduler email service is working."
    )

    return {
        "message": "Email sent successfully"
    }