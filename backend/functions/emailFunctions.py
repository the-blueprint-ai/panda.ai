from fastapi import Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from config import settings
import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from python_http_client.exceptions import HTTPError


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

        # Send an HTTP POST request to /mail/send
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

        return{"Email sent successfully"}
    
    except HTTPError as e:
        print(e.to_dict)
