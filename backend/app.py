import uvicorn

from fastapi import FastAPI, Depends, File, UploadFile, Path, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from cryptography.fernet import Fernet
import hashlib
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

S3_BUCKET = "panda.ai"
s3 = boto3.client('s3', aws_access_key_id = 'AKIA4M7OWVUMBL3LUZ5D', aws_secret_access_key = '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')

DATABASE_URL = 'postgres://panda_ai:OtR2wwJ5mF3ncFg8AALK@panda-ai-psql-instance-1.cckdg1c2elzf.eu-west-2.rds.amazonaws.com:5432/panda_ai'
database = Database(DATABASE_URL)

# Generate a key or load it from a secure location
# key = Fernet.generate_key()
# print(key.decode('utf-8'))
key = 'tMPgiGpTAYajir4Btprcp4cdHuI5svtU0T7ufLoHVPM=' #os.environ.get("FERNET_KEY")
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

app = FastAPI(title="panda.ai")
app.add_middleware(get_middleware())

# Connect/Disconnect from Aurora
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Catch exceptions
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(content={"error": str(exc)}, status_code=400)

# Functions & Classes
async def save_user_data(user_id: str, first_name: str, last_name: str, username: str, email: str):
    # Encrypt the input values
    encrypted_first_name = cipher_suite.encrypt(first_name.encode()).decode('utf-8')
    encrypted_last_name = cipher_suite.encrypt(last_name.encode()).decode('utf-8')
    encrypted_username = cipher_suite.encrypt(username.encode()).decode('utf-8')
    encrypted_email = cipher_suite.encrypt(email.encode()).decode('utf-8')

    query = """
        INSERT INTO panda_ai_users (user_id, first_name, last_name, username, email)
        VALUES (:user_id, :first_name, :last_name, :username, :email)
    """
    values = {
        "user_id": user_id,
        "first_name": encrypted_first_name,
        "last_name": encrypted_last_name,
        "username": encrypted_username,
        "email": encrypted_email
    }
    await database.execute(query=query, values=values)

async def get_user_data(user_id: str):
    query = "SELECT user_id, first_name, last_name, username, email FROM panda_ai_users WHERE user_id = :user_id"
    values = {"user_id": user_id}
    result = await database.fetch_one(query=query, values=values)

    if result:
        decrypted_first_name = cipher_suite.decrypt(result["first_name"].encode()).decode('utf-8')
        decrypted_last_name = cipher_suite.decrypt(result["last_name"].encode()).decode('utf-8')
        decrypted_username = cipher_suite.decrypt(result["username"].encode()).decode('utf-8')
        decrypted_email = cipher_suite.decrypt(result["email"].encode()).decode('utf-8')

        return {
            "user_id": user_id,
            "first_name": decrypted_first_name,
            "last_name": decrypted_last_name,
            "username": decrypted_username,
            "email": decrypted_email
        }
    else:
        return None

class UserData(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    username: str
    email: str

# APIs
@app.post("/save-user-data/")
async def save_user_data_route(user_data: UserData):
    try:
        await save_user_data(user_data.user_id, user_data.first_name, user_data.last_name, user_data.username, user_data.email)
        return {"message": "Data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_user_data/")
async def get_user_data_route(user_id: str):
    try:
        data = await get_user_data(user_id)
        if data:
            return data
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Error in get_data_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/sessioninfo")    
async def secure_api(s: SessionContainer = Depends(verify_session())):
    return {
        "sessionHandle": s.get_handle(),
        "userId": s.get_user_id(),
        "accessTokenPayload": s.get_access_token_payload(),
    }

@app.post("/uploadimage/")
async def upload_file(userid: str, file: UploadFile = File(...)):
    try:
        # Read the file content
        content = await file.read()

        folder = f'{userid}/avatar/avatar'
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
            "url": f"https://{S3_BUCKET}.s3.amazonaws.com/{folder}{file_extension}",
        }
        return JSONResponse(content=response, status_code=200)

    except Exception as e:
        response = {"error": str(e)}
        return JSONResponse(content=response, status_code=400)
    
@app.get("/getimage/")
async def download_file(userid):
    try:
        prefix = f'{userid}/avatar/avatar'

        # Search for files with the specified prefix in the S3 bucket
        s3_response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)

        if "Contents" not in s3_response or not s3_response["Contents"]:
            raise HTTPException(status_code=404, detail="File not found")

        # Extract file names from the S3 response
        file_name = [obj["Key"] for obj in s3_response["Contents"]]

        # Convert file_name to string
        key = "".join(file_name)

        # Get the file from S3
        s3_file = s3.get_object(Bucket=S3_BUCKET, Key=key)

        # Create a StreamingResponse to send the file content to the client
        response = StreamingResponse(
            s3_file["Body"], headers={"Content-Type": s3_file["ContentType"]}
        )

        return response

    except Exception as e:
        return {"error": str(e)}

@app.get("/test")
async def root():
    return {"message": "Hello World"}

# Middleware
app = CORSMiddleware(
    app=app,
    allow_origins=[config.app_info.website_domain],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

if __name__  == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
