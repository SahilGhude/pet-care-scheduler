from brevo import AsyncBrevo
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)
from pydantic import EmailStr
from dotenv import load_dotenv
import os

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
MAIL_FROM = os.getenv("MAIL_FROM")

client = AsyncBrevo(api_key=BREVO_API_KEY)


async def send_email(
    email: EmailStr,
    subject: str,
    body: str
):
    result = await client.transactional_emails.send_transac_email(
        subject=subject,
        text_content=body,
        sender=SendTransacEmailRequestSender(
            email=MAIL_FROM,
            name="Pet Care Scheduler"
        ),
        to=[
            SendTransacEmailRequestToItem(
                email=str(email)
            )
        ]
    )

    print("Email sent successfully:", result.message_id)