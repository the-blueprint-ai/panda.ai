from uvicorn import Config, Server
from functools import lru_cache
from config import settings
from fastapi_utils.tasks import repeat_every

from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet
from starlette.middleware.cors import CORSMiddleware

from supertokens_python import init, get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

import boto3
from io import BytesIO
import os
import logging
from databases import Database
import config

from routers import users
from routers import entities
from routers import chats
from routers import gpt
from routers import roadmap
from routers import admin
from routers import faqs
from routers import email
from routers import subscriptions
from routers import webhooks

from functions.repeatedFunctions import Ping

@lru_cache()
def get_settings():
    return config.Settings()

S3_BUCKET = settings.S3_BUCKET #"panda.ai"
s3 = boto3.client('s3', aws_access_key_id = settings.AWS_ACCESS_KEY_ID, aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY)

DATABASE_URL = settings.PSQL_DATABASE_URL
database = Database(DATABASE_URL)

key = settings.FERNET_KEY
if not key:
    raise ValueError("FERNET_KEY environment variable not set")
cipher_suite = Fernet(key.encode())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

init(
    supertokens_config=config.supertokens_config,
    app_info=config.app_info,
    framework=config.framework,
    recipe_list=config.recipe_list,
    mode="asgi",
)

app = FastAPI(title="panda.ai", version="0.1.1")
app.include_router(users.router)
app.include_router(entities.router)
app.include_router(chats.router)
app.include_router(gpt.router)
app.include_router(roadmap.router)
app.include_router(admin.router)
app.include_router(faqs.router)
app.include_router(email.router)
app.include_router(subscriptions.router)
app.include_router(webhooks.router)
app.add_middleware(get_middleware())

@app.on_event("startup")
@repeat_every(wait_first = True, seconds=60, max_repetitions=5)  # 1 minute
def ping_task() -> None:
    Ping()


# Catch exceptions
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(content={"error": str(exc)}, status_code=400)


# Session Info API
@app.get("/sessioninfo")    
async def secure_api(s: SessionContainer = Depends(verify_session())):
    return {
        "sessionHandle": s.get_handle(),
        "userId": s.get_user_id(),
        "accessTokenPayload": s.get_access_token_payload(),
    }

# Test API
@app.get("/test")
async def root():
    return {"message": "Hello World"}

# Avatar Image APIs
@app.post("/uploadimage/")
async def upload_file(userid: str, file: UploadFile = File(...)):
    try:
        # Read the file content
        content = await file.read()

        folder = f'{userid}/profile/avatar'
        file_name, file_extension = os.path.splitext(file.filename)

        # Upload the file to S3
        s3.upload_fileobj(
            Fileobj=BytesIO(content),  # Convert the content to a file-like object
            Bucket=S3_BUCKET,
            Key=folder + file_extension,
        )

        # Return the public URL of the uploaded file
        response = {
            "message": "Image uploaded successfully",
            "url": f"https://s3.eu-west-2.amazonaws.com/{S3_BUCKET}/{folder}{file_extension}"
        }
        return JSONResponse(content=response, status_code=200)

    except Exception as e:
        response = {"error": str(e)}
        return JSONResponse(content=response, status_code=400)


# Middleware
app = CORSMiddleware(
    app=app,
    allow_origins=[config.app_info.website_domain],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

if __name__ == "__main__":
    uvicorn_config = Config(
        "app:app",
        host="0.0.0.0",
        port=3001,
        log_level="info",
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "loggers": {
                "uvicorn.error": {"level": "ERROR"},
                "uvicorn.access": {"level": "INFO"},
            },
        },
    )
    server = Server(config=uvicorn_config)
    server.run()
