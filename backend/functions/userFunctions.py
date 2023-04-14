from fastapi import HTTPException, UploadFile, File, Depends
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.asyncio import delete_user
from config import settings
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet
from databases import Database
import logging
import boto3
from functions.helperFunctions import get_user_data, save_user_data, save_user_banner, save_user_avatar


# DATABASES
S3_BUCKET = settings.S3_BUCKET #"panda.ai"
s3 = boto3.client('s3', aws_access_key_id = settings.AWS_ACCESS_KEY_ID, aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    

key = settings.FERNET_KEY
if not key:
    raise ValueError("FERNET_KEY environment variable not set")
cipher_suite = Fernet(key.encode())

# FUNCTIONS
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


async def do_delete(user_id: str, session: SessionContainer = Depends(verify_session())):
    await delete_user(user_id) # this will succeed even if the userId didn't exist.


async def save_user_data_route(user_id, first_name=None, last_name=None, username=None, email=None, avatar=None, banner=None, about=None, onboarded=None, subscriber=None, admin=None, session: SessionContainer = Depends(verify_session())):
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