from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.asyncio import delete_user
from pydantic import ValidationError
from config import settings
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet
from databases import Database
import logging
import boto3
from io import BytesIO
import os

# CONFIG
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

S3_BUCKET = settings.S3_BUCKET #"panda.ai"
s3 = boto3.client('s3', aws_access_key_id = settings.AWS_ACCESS_KEY_ID, aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY)

DATABASE_URL = settings.PSQL_DATABASE_URL
database = Database(DATABASE_URL)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

key = settings.FERNET_KEY
if not key:
    raise ValueError("FERNET_KEY environment variable not set")
cipher_suite = Fernet(key.encode())


# Connect/Disconnect from Aurora
@router.on_event("startup")
async def startup():
    await database.connect()

@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


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
async def save_user_data_route(user_id, first_name, last_name, username, email, avatar, session: SessionContainer = Depends(verify_session())):
    try:
        response = await save_user_data(user_id, first_name, last_name, username, email, avatar)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return {"message": "User data saved successfully"}
    except HTTPException as e:
        logger.error(f"HTTPException in save_user_data_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in save_user_data_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.post("/update")
async def update_user_data_route(user_id, first_name, last_name, username, email, session: SessionContainer = Depends(verify_session())):
    try:
        response = await update_user_data(user_id, first_name, last_name, username, email)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return {"message": "User data updated successfully"}
    except HTTPException as e:
        logger.error(f"HTTPException in update_user_data_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in update_user_data_route: {e}, type: {type(e)}, args: {e.args}")
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
        decrypted_first_name = cipher_suite.decrypt(result["first_name"].encode()).decode('utf-8')
        decrypted_last_name = cipher_suite.decrypt(result["last_name"].encode()).decode('utf-8')
        decrypted_username = cipher_suite.decrypt(result["username"].encode()).decode('utf-8')
        decrypted_email = cipher_suite.decrypt(result["email"].encode()).decode('utf-8')
        avatar = result["avatar"]
        banner = result["banner"]
        about = result["about"]
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
            "about": about,
            "onboarded": onboarded,
            "subscriber": subscriber,
            "admin": admin,
        }
    else:
        return None

async def save_user_data(user_id: str, first_name: str, last_name: str, username: str, email: str, avatar: str):
    # Encrypt the input values
    encrypted_first_name = cipher_suite.encrypt(first_name.encode()).decode('utf-8')
    encrypted_last_name = cipher_suite.encrypt(last_name.encode()).decode('utf-8')
    encrypted_username = cipher_suite.encrypt(username.encode()).decode('utf-8')
    encrypted_email = cipher_suite.encrypt(email.encode()).decode('utf-8')

    query = """
        INSERT INTO panda_ai_users (user_id, first_name, last_name, username, email, avatar)
        VALUES (:user_id, :first_name, :last_name, :username, :email, :avatar)
    """
    values = {
        "user_id": user_id,
        "first_name": encrypted_first_name,
        "last_name": encrypted_last_name,
        "username": encrypted_username,
        "email": encrypted_email,
        "avatar": avatar
    }
    await database.execute(query=query, values=values)

async def update_user_data(user_id: str, first_name: str, last_name: str, username: str, email: str):
    # Encrypt the input values
    encrypted_first_name = cipher_suite.encrypt(first_name.encode()).decode('utf-8')
    encrypted_last_name = cipher_suite.encrypt(last_name.encode()).decode('utf-8')
    encrypted_username = cipher_suite.encrypt(username.encode()).decode('utf-8')
    encrypted_email = cipher_suite.encrypt(email.encode()).decode('utf-8')

    query = """
        UPDATE panda_ai_users 
        SET first_name = :first_name, last_name = :last_name, username = :username, email = :email
        WHERE user_id = :user_id
    """
    values = {
        "user_id": user_id,
        "first_name": encrypted_first_name,
        "last_name": encrypted_last_name,
        "username": encrypted_username,
        "email": encrypted_email
    }
    await database.execute(query=query, values=values)
    
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

    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        return response
    
    except Exception as e:
        response = {"error": str(e)}
        return response
    
    return response
