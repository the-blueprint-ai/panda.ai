from fastapi import Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from config import settings
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FUNCTIONS
async def email_send(from_email: str, to_emails: str, subject: str, html_content: str):
    message = Mail(
    from_email=from_email,
    to_emails=to_emails,
    subject=subject,
    html_content=html_content)

    try:
        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

        response = sg.send(message)

        return{"Email sent successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while trying to send email: {e}")

async def add_contact(user_id: str, email: str):

    data = {
        "contacts": [
            {
                "email": email,
                "custom_fields": {
                    "e1_T": user_id
                }
            }
        ]
    }

    try:
        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

        response = sg.client.marketing.contacts.put(
            request_body=data
        )

        return{"Email saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while trying to send email: {e}")
