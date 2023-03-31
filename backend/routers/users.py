from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.asyncio import delete_user
from pydantic import ValidationError
from config import settings
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet, InvalidToken
from databases import Database
import logging
from typing import Optional
import boto3
from io import BytesIO
import os

# CONFIG
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# DATABASES
S3_BUCKET = settings.S3_BUCKET #"panda.ai"
s3 = boto3.client('s3', aws_access_key_id = settings.AWS_ACCESS_KEY_ID, aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY)

DATABASE_URL = settings.PSQL_DATABASE_URL
database = Database(DATABASE_URL)

# Connect/Disconnect from Aurora
@router.on_event("startup")
async def startup():
    await database.connect()

@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

key = settings.FERNET_KEY
if not key:
    raise ValueError("FERNET_KEY environment variable not set")
cipher_suite = Fernet(key.encode())


# ROUTERS
@router.get("/get")
async def get_user_data_route(user_id: str, session: SessionContainer = Depends(verify_session())):
    try:
        response = await get_user_data(user_id)
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException as e:
        logger.error(f"HTTPException in get_user_data_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in get_data_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/delete")
async def do_delete(user_id: str, session: SessionContainer = Depends(verify_session())):
    await delete_user(user_id) # this will succeed even if the userId didn't exist.

@router.post("/save")
async def save_user_data_route(user_id, first_name=None, last_name=None, username=None, email=None, avatar=None, banner=None, about=None, onboarded=None, subscriber=None, admin=None):
    # Convert 'onboarded', 'subscriber', and 'admin' to boolean values
    onboarded = onboarded.lower() == "true" if onboarded is not None else None
    subscriber = subscriber.lower() == "true" if subscriber is not None else None
    admin = admin.lower() == "true" if admin is not None else None
    try:
        response = await save_user_data(user_id, first_name, last_name, username, email, avatar, banner, about, onboarded, subscriber, admin)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return {"message": "User data saved successfully"}
    except HTTPException as e:
        logger.error(f"HTTPException in save_user_data_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in save_user_data_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.post("/banner")
async def save_user_banner_route(user_id: str, file: UploadFile = File(...), session: SessionContainer = Depends(verify_session())):
    try:
        response = await save_user_banner(user_id, file)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return {"message": "Banner saved successfully", "url": response["url"]}
    except HTTPException as e:
        logger.error(f"HTTPException in save_user_banner_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in save_user_banner_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.post("/avatar")
async def save_user_avatar_route(user_id: str, file: UploadFile = File(...), session: SessionContainer = Depends(verify_session())):
    try:
        response = await save_user_avatar(user_id, file)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return {"message": "Avatar saved successfully", "url": response["url"]}
    except HTTPException as e:
        logger.error(f"HTTPException in save_user_avatar_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in save_user_avatar_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


# FUNCTIONS
async def get_user_data(user_id: str):
    query = "SELECT user_id, created_at, first_name, last_name, username, email, avatar, banner, about, onboarded, subscriber, admin FROM panda_ai_users WHERE user_id = :user_id"
    values = {"user_id": user_id}
    result = await database.fetch_one(query=query, values=values)

    if result:
        created_at = result["created_at"]
        try:
            decrypted_first_name = decrypt_if_not_none(result["first_name"])
            decrypted_last_name = decrypt_if_not_none(result["last_name"])
            decrypted_username = decrypt_if_not_none(result["username"])
            decrypted_email = decrypt_if_not_none(result["email"])
            decrypted_about = decrypt_if_not_none(result["about"])

        except InvalidToken:
            return {"error": "Error decrpyting user data"}

        avatar = result["avatar"]
        banner = result["banner"]
        onboarded = result["onboarded"]
        subscriber = result["subscriber"]
        admin = result["admin"]
        

        return {
            "user_id": user_id,
            "created_at": created_at,
            "first_name": decrypted_first_name,
            "last_name": decrypted_last_name,
            "username": decrypted_username,
            "email": decrypted_email,
            "avatar": avatar,
            "banner": banner,
            "about": decrypted_about,
            "onboarded": onboarded,
            "subscriber": subscriber,
            "admin": admin,
        }
    else:
        return None
    
def decrypt_if_not_none(value):
    if value is not None:
        return cipher_suite.decrypt(value.encode()).decode('utf-8')
    return None

async def save_user_data(user_id: str, first_name: Optional[str] = None, last_name: Optional[str] = None, username: Optional[str] = None, email: Optional[str] = None, avatar: Optional[str] = None, banner: Optional[str] = None, about: Optional[str] = None, onboarded: Optional[bool] = None, subscriber: Optional[bool] = None, admin: Optional[bool] = None):
    # Fetch the existing user data from the database
    existing_user_data = await get_user_data(user_id)

    # If the existing user data is None, the user does not exist, so insert a new user
    if existing_user_data is None:
        return await save_new_user_data(user_id, first_name, last_name, username, email, avatar, banner, about, onboarded, subscriber, admin)

    # If there's an error in the existing user data, handle it accordingly
    if existing_user_data is None or "error" in existing_user_data:
        # Handle the error according to your application's requirements, e.g., raise an exception or return an error message
        raise Exception("Error fetching existing user data")

    # Prepare the query and the values dictionary
    query = "UPDATE panda_ai_users SET"
    values = {"user_id": user_id}
    fields_to_update = []

    # Add fields to the query and the values dictionary only if they have new values
    if first_name is not None:
        fields_to_update.append("first_name = :first_name")
        values["first_name"] = encrypt_if_not_none(first_name)

    if last_name is not None:
        fields_to_update.append("last_name = :last_name")
        values["last_name"] = encrypt_if_not_none(last_name)

    if username is not None:
        fields_to_update.append("username = :username")
        values["username"] = encrypt_if_not_none(username)

    if email is not None:
        fields_to_update.append("email = :email")
        values["email"] = encrypt_if_not_none(email)

    if avatar is not None:
        fields_to_update.append("avatar = :avatar")
        values["avatar"] = avatar

    if banner is not None:
        fields_to_update.append("banner = :banner")
        values["banner"] = banner

    if about is not None:
        fields_to_update.append("about = :about")
        values["about"] = encrypt_if_not_none(about)

    if onboarded is not None:
        fields_to_update.append("onboarded = :onboarded")
        values["onboarded"] = onboarded
    else:
        fields_to_update.append("onboarded = :onboarded")
        values["onboarded"] = False

    if subscriber is not None:
        fields_to_update.append("subscriber = :subscriber")
        values["subscriber"] = subscriber
    else:
        fields_to_update.append("subscriber = :subscriber")
        values["subscriber"] = False

    if admin is not None:
        fields_to_update.append("admin = :admin")
        values["admin"] = admin
    else:
        fields_to_update.append("admin = :admin")
        values["admin"] = False

    # Join the fields to update and add the WHERE clause to the query
    query += " " + ", ".join(fields_to_update) + " WHERE user_id = :user_id"
    
    await database.execute(query=query, values=values)
    return {"message": "User data updated successfully"}

def encrypt_if_not_none(value: Optional[str]) -> Optional[str]:
    if value is not None:
        return cipher_suite.encrypt(value.encode()).decode('utf-8')
    return None

async def save_new_user_data(user_id: str, first_name: Optional[str] = None, last_name: Optional[str] = None, username: Optional[str] = None, email: Optional[str] = None, avatar: Optional[str] = None, banner: Optional[str] = None, about: Optional[str] = None, onboarded: Optional[bool] = None, subscriber: Optional[bool] = None, admin: Optional[bool] = None):
    if onboarded is None:
        onboarded = False
    if subscriber is None:
        subscriber = False
    if admin is None:
        admin = False

    values = {
        "user_id": user_id,
        "first_name": encrypt_if_not_none(first_name),
        "last_name": encrypt_if_not_none(last_name),
        "username": encrypt_if_not_none(username),
        "email": encrypt_if_not_none(email),
        "avatar": avatar,
        "banner": banner,
        "about": encrypt_if_not_none(about),
        "onboarded": onboarded,
        "subscriber": subscriber,
        "admin": admin
    }

    query = """
        INSERT INTO panda_ai_users (user_id, first_name, last_name, username, email, avatar, banner, about, onboarded, subscriber, admin)
        VALUES (:user_id, :first_name, :last_name, :username, :email, :avatar, :banner, :about, :onboarded, :subscriber, :admin)
    """

    await database.execute(query=query, values=values)
    return {"message": "User data inserted successfully"}
    
async def save_user_banner(user_id: str, file: UploadFile = File(...)):
    try:
        # Read the file content
        content = await file.read()

        folder = f'{user_id}/profile/banner'
        file_name, file_extension = os.path.splitext(file.filename)

        # Upload the file to S3
        s3.upload_fileobj(
            Fileobj=BytesIO(content),  # Convert the content to a file-like object
            Bucket=S3_BUCKET,
            Key=folder + file_extension,
        )

        # Return the public URL of the uploaded file
        response = {
            "message": "Banner uploaded successfully",
            "url": f"https://s3.eu-west-2.amazonaws.com/{S3_BUCKET}/{folder}{file_extension}",
        }
        banner = response["url"]
    
        query = """
            UPDATE panda_ai_users SET banner = :banner WHERE user_id = :user_id
        """
        values = {
            "user_id": user_id,
            "banner": banner
        }
        await database.execute(query=query, values=values)
        return {"message": "User banner updated successfully", "url": banner}

    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        return response
    
    except Exception as e:
        response = {"error": str(e)}
        return response

    return response

async def save_user_avatar(user_id: str, file: UploadFile = File(...)):
    try:
        # Read the file content
        content = await file.read()

        folder = f'{user_id}/profile/avatar'
        file_name, file_extension = os.path.splitext(file.filename)

        # Upload the file to S3
        s3.upload_fileobj(
            Fileobj=BytesIO(content),  # Convert the content to a file-like object
            Bucket=S3_BUCKET,
            Key=folder + file_extension,
        )

        # Return the public URL of the uploaded file
        response = {
            "message": "Avatar uploaded successfully",
            "url": f"https://s3.eu-west-2.amazonaws.com/{S3_BUCKET}/{folder}{file_extension}",
        }
        avatar = response["url"]
    
        query = """
            UPDATE panda_ai_users SET avatar = :avatar WHERE user_id = :user_id
        """
        values = {
            "user_id": user_id,
            "avatar": avatar
        }
        await database.execute(query=query, values=values)
        return {"message": "User avatar updated successfully", "url": avatar}

    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        return response
    
    except Exception as e:
        response = {"error": str(e)}
        return response
    
    return response
