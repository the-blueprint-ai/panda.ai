from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Request
from dependencies import database
from event_utils import register_events
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.thirdpartyemailpassword.syncio import get_user_by_id, emailpassword_sign_in, update_email_or_password
from supertokens_python.recipe.session.syncio import revoke_all_sessions_for_user
from supertokens_python.recipe.thirdpartyemailpassword.interfaces import EmailPasswordSignInWrongCredentialsError
from supertokens_python.asyncio import delete_user
from pydantic import ValidationError, BaseModel
from config import settings
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet, InvalidToken
from databases import Database
import logging, asyncio, hashlib, os, boto3
from typing import Optional, Any, List
from io import BytesIO
from functions.entityFunctions import delete_entity
from functions.subscriptionFunctions import cancel_subscription

# CONFIG
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

register_events(router)

# DATABASES
S3_BUCKET = settings.S3_BUCKET
s3 = boto3.client('s3', aws_access_key_id = settings.AWS_ACCESS_KEY_ID, aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

key = settings.FERNET_KEY
if not key:
    raise ValueError("FERNET_KEY environment variable not set")
cipher_suite = Fernet(key.encode())

# DATA MODELS
class IntegrationData(BaseModel):
    user_id: str
    selected_integrations: List[int]


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
    try:
        response = await asyncio.gather(
            delete_user(user_id), # this will succeed even if the userId didn't exist.
            delete_internal_user(user_id, session)
        )   
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException as e:
        logger.error(f"HTTPException in delete_user: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in delete_user: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.get("/get-integrations") 
async def get_integrations_route(userId: str, session: SessionContainer = Depends(verify_session())):
    try:
        response = await get_integrations(userId)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return response
    except HTTPException as e:
        logger.error(f"HTTPException in get_integrations_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in get_integrations_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/get-integrations-list") 
async def get_integrations_list_route(session: SessionContainer = Depends(verify_session())):
    try:
        response = await get_integrations_list()
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return response
    except HTTPException as e:
        logger.error(f"HTTPException in get_integrations_list_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in get_integrations_list_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

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
    
@router.post("/change-password") 
def update_password_route(oldPassword: str, newPassword: str, session: SessionContainer = Depends(verify_session())):
    try:
        response = update_password(oldPassword, newPassword, session)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return {"message": "Password updated successfully"}
    except HTTPException as e:
        logger.error(f"HTTPException in update_password_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in update_password_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/change-email") 
def update_email_route(user_id: str, new_email: str, session: SessionContainer = Depends(verify_session())):
    try:
        response = update_email(user_id, new_email)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return {"message": "Email updated successfully"}
    except HTTPException as e:
        logger.error(f"HTTPException in update_email_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in update_email_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.get("/get-onboarded") 
async def get_onboarded_route(userId: str, session: SessionContainer = Depends(verify_session())):
    try:
        response = await get_onboarded(userId)
        return response
    except HTTPException as e:
        logger.error(f"HTTPException in get_onboarded_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in get_onboarded_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/set-onboarded") 
async def set_onboarded_route(userId: str, session: SessionContainer = Depends(verify_session())):
    try:
        response = await set_onboarded(userId)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return {"message": "User onboarded successfully"}
    except HTTPException as e:
        logger.error(f"HTTPException in set_onboarded_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in set_onboarded_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.post("/set-integrations") 
async def set_integrations_route(integration_data: IntegrationData, session: SessionContainer = Depends(verify_session())):
    try:
        response = await set_integrations(integration_data.user_id, integration_data.selected_integrations)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return {"message": "User integrations updated successfully"}
    except HTTPException as e:
        logger.error(f"HTTPException in set_integrations_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in set_integrations_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

# FUNCTIONS
async def get_user_data(user_id: str):
    query = "SELECT user_id, created_at, first_name, last_name, username, email, avatar, banner, about, onboarded, subscriber, admin, subscribed_at, integrations, messages_per_month, subscriber_id, plan_id FROM panda_ai_users WHERE user_id = :user_id"
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
        subscribed_at = result["subscribed_at"]
        integrations = result["integrations"]
        messages_per_month = result["messages_per_month"]
        subscriber_id = result["subscriber_id"]
        plan_id = result["plan_id"]

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
            "subscribed_at": subscribed_at,
            "integrations": integrations,
            "messages_per_month": messages_per_month,
            "subscriber_id": subscriber_id,
            "plan_id": plan_id,
        }
    else:
        return None
    
def hash_username(username: str) -> bytes:
    return hashlib.sha256(username.encode()).digest()

def encrypt_if_not_none(value: Optional[str]) -> Optional[str]:
    if value is not None:
        return cipher_suite.encrypt(value.encode()).decode('utf-8')
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
        fields_to_update.append("hashed_username = :hashed_username")
        values["username"] = encrypt_if_not_none(username)
        values["hashed_username"] = hash_username(username)

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

    if subscriber is not None:
        fields_to_update.append("subscriber = :subscriber")
        values["subscriber"] = subscriber

    if admin is not None:
        fields_to_update.append("admin = :admin")
        values["admin"] = admin

    # Join the fields to update and add the WHERE clause to the query
    query += " " + ", ".join(fields_to_update) + " WHERE user_id = :user_id"
    
    await database.execute(query=query, values=values)
    return {"message": "User data updated successfully"}


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
    

async def delete_internal_user(user_id: str, session: SessionContainer = Depends(verify_session())):
    try:
        response = await asyncio.gather(
            delete_user_chat_history(user_id),
            delete_entity(user_id),
            delete_user_integrations(user_id),
            delete_user_messages(user_id),
            delete_user_subscription(user_id),
            delete_user_s3(user_id)
        ) 

        query = """
            DELETE FROM panda_ai_users WHERE user_id = :user_id
        """
        values = {
            "user_id": user_id
        }
        await database.execute(query=query, values=values)

        # revoke all sessions for the user
        await revoke_all_sessions_for_user(user_id)
        # revoke the user's current session, we do this to remove the auth cookies, logging out the user on the frontend
        session.sync_revoke_session()

        return {"message": "User deleted successfully"}

    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        return response
    
    except Exception as e:
        response = {"error": str(e)}
        return response


async def delete_user_chat_history(user_id: str):
    query = "DELETE FROM panda_ai_user_chat_history WHERE user_id = :user_id"
    values = {"user_id": user_id}
    try:
        results = await database.execute(query=query, values=values)

        if results:
            logging.info(f"Deleted {results} chat history record(s) for user {user_id}")
            return {"message": f"Deleted {results} chat history record(s) successfully"}
        else:
            logging.info(f"No chat history found for user {user_id}")
            return {"message": f"No chat history found for user {user_id}"}
    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        logging.error(f"Validation error while deleting chat history for user {user_id}: {response}")
        return response
    except Exception as e:
        response = {"error": str(e)}
        logging.error(f"Exception while deleting chat history for user {user_id}: {str(e)}")
        return response

async def delete_user_integrations(user_id: str):
    query = "DELETE FROM panda_ai_user_integrations WHERE user_id = :user_id"
    values = {"user_id": user_id}
    try:
        results = await database.execute(query=query, values=values)

        if results:
            logging.info(f"Deleted {results} integration(s) for user {user_id}")
            return {"message": f"Deleted {results} integration(s) successfully"}
        else:
            logging.info(f"No integrations found for user {user_id}")
            return {"message": f"No integrations found for user {user_id}"}
    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        logging.error(f"Validation error while deleting integrations for user {user_id}: {response}")
        return response
    except Exception as e:
        response = {"error": str(e)}
        logging.error(f"Exception while deleting integrations for user {user_id}: {str(e)}")
        return response
    
async def delete_user_messages(user_id: str):
    query = "DELETE FROM panda_ai_messages WHERE user_id = :user_id"
    values = {"user_id": user_id}
    try:
        results = await database.execute(query=query, values=values)

        if results:
            logging.info(f"Deleted {results} message(s) for user {user_id}")
            return {"message": f"Deleted {results} message(s) successfully"}
        else:
            logging.info(f"No messages found for user {user_id}")
            return {"message": f"No messages found for user {user_id}"}
    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        logging.error(f"Validation error while deleting messages for user {user_id}: {response}")
        return response
    except Exception as e:
        response = {"error": str(e)}
        logging.error(f"Exception while deleting messages for user {user_id}: {str(e)}")
        return response
    
async def delete_user_subscription(user_id: str):
    await cancel_subscription(user_id)
    logging.info(f"User {user_id}'s subscriptions cancelled successfully from Stripe")

    query = "DELETE FROM panda_ai_user_subscriptions WHERE user_id = :user_id"
    values = {"user_id": user_id}
    try:
        results = await database.execute(query=query, values=values)

        if results:
            logging.info(f"Deleted {results} subscription(s) for user {user_id} in the database")
            return {"message": f"Deleted {results} subscription(s) successfully"}
        else:
            logging.info(f"No subscriptions found for user {user_id} in the database")
            return {"message": f"No subscriptions found for user {user_id}"}
    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        logging.error(f"Validation error while deleting subscriptions for user {user_id}: {response}")
        return response
    except Exception as e:
        response = {"error": str(e)}
        logging.error(f"Exception while deleting subscriptions for user {user_id}: {str(e)}")
        return response
    
async def delete_user_s3(user_id:str):
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=user_id)
        if 'Contents' in response:
            objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
            s3.delete_objects(Bucket=S3_BUCKET, Delete={'Objects': objects_to_delete})
    
    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        logging.error(f"Validation error while deleting subscriptions for user {user_id}: {response}")
        return response
    except Exception as e:
        response = {"error": str(e)}
        logging.error(f"Exception while deleting subscriptions for user {user_id}: {str(e)}")
        return response

def update_password(oldPassword: str, newPassword: str, session: SessionContainer = Depends(verify_session())):
    try:
         # get the userId from the session object
        user_id = session.get_user_id()

        # get the signed in user's email from the getUserById function
        users_info = get_user_by_id(user_id)

        if users_info is None:
            raise Exception("Should never come here")
        
        isPasswordValid = emailpassword_sign_in(users_info.email, oldPassword) 

        if isinstance(isPasswordValid, EmailPasswordSignInWrongCredentialsError):
            return {"message": "Current password incorrect"}

        # update the users password
        update_email_or_password(user_id, password=newPassword)

        # revoke all sessions for the user
        revoke_all_sessions_for_user(user_id)
        
        # revoke the user's current session, we do this to remove the auth cookies, logging out the user on the frontend
        session.sync_revoke_session()

        return {"message": "Password updated successfully"}

    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        return response
    
    except Exception as e:
        response = {"error": str(e)}
        return response

def update_email(user_id: str, new_email: str):
    try:
        # update the users password
        update_email_or_password(user_id, email=new_email)

        return {"message": "Email updated successfully"}

    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        return response
    
    except Exception as e:
        response = {"error": str(e)}
        return response


async def get_onboarded(user_id: str):
    try:
        query = """
            SELECT onboarded
            FROM panda_ai_users 
            WHERE user_id = :user_id
        """
        values = {
            "user_id": user_id
        }
        response = await database.execute(query=query, values=values)
        return response

    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        return response
    
    except Exception as e:
        response = {"error": str(e)}
        return response


async def set_onboarded(user_id: str):
    try:
        query = """
            UPDATE panda_ai_users 
            SET onboarded = true , subscriber = true, onboarded_at = NOW(), messages_per_month = 20, integrations = 8
            WHERE user_id = :user_id
        """
        values = {
            "user_id": user_id
        }
        await database.execute(query=query, values=values)
        integrations = {1, 2, 3, 4, 5, 6, 7, 8}
        await set_integrations(user_id, integrations)
        return {"message": "User set as onboarded successfully"}

    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        return response
    
    except Exception as e:
        response = {"error": str(e)}
        return response
    
async def get_integrations(user_id: str):
    query = "SELECT integration_id, last_updated FROM panda_ai_user_integrations WHERE user_id = :user_id"
    values = {"user_id": user_id}
    result = await database.fetch_all(query=query, values=values)

    if result:
        integrations = []
        for row in result:
            integrations.append({
                "integration_id": row["integration_id"],
                "last_updated": row["last_updated"],
            })
        return integrations
    else:
        response = {"message": "No integrations found"}
        return response
    
async def set_integrations(user_id: str, selected_integrations: list):
    # Start by deleting all existing rows for this user
    delete_query = "DELETE FROM panda_ai_user_integrations WHERE user_id = :user_id"
    await database.execute(query=delete_query, values={"user_id": user_id})

    # Then, insert the new integrations
    for integration_id in selected_integrations:
        insert_query = """
        INSERT INTO panda_ai_user_integrations (user_id, integration_id, last_updated) 
        VALUES (:user_id, :integration_id, NOW())
        """
        values = {"user_id": user_id, "integration_id": integration_id}
        await database.execute(query=insert_query, values=values)

    # If code reaches this point, it means all operations were successful
    return {"message": "Integrations updated successfully"}

async def get_integrations_list():
    query = "SELECT * FROM panda_ai_integrations"
    result = await database.fetch_all(query=query)

    if result:
        integrations_list = []
        for row in result:
            integrations_list.append({
                "integration_id": row["integration_id"],
                "integration_name": row["integration_name"],
                "integration_icon": row["integration_icon"],
            })
        return integrations_list
    else:
        response = {"message": "No integrations list found"}
        return response