from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
import secrets
import logging
from config import settings

# CONFIG
router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
)

security = HTTPBasic()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FUNCTIONS
def verify_credentials(credentials: Optional[HTTPBasicCredentials] = Depends(security)) -> bool:
    correct_username = settings.WEBHOOKS_USERNAME
    correct_password = settings.WEBHOOKS_PASSWORD

    if not credentials:
        return False

    if not (secrets.compare_digest(credentials.username, correct_username) and
            secrets.compare_digest(credentials.password, correct_password)):
        return False

    return True


# ROUTERS
@router.post("/customer-created")
async def receive_webhook(request: Request, authenticated: bool = Depends(verify_credentials)):
    if not authenticated:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    payload = await request.json()
    logging.info("Customer Created Webhook received:", str(payload))
    return {"detail": "Webhook received"}

@router.post("/subscribe")
async def receive_webhook(request: Request, authenticated: bool = Depends(verify_credentials)):
    if not authenticated:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    payload = await request.json()
    logging.info("Subscribe Webhook received:", str(payload))
    return {"detail": "Webhook received"}

@router.post("/unsubscribe")
async def receive_webhook(request: Request, authenticated: bool = Depends(verify_credentials)):
    if not authenticated:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    payload = await request.json()
    logging.info("Unsubscribe Webhook received:", str(payload))
    return {"detail": "Webhook received"}



