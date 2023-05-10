from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Optional
import secrets
import logging
from datetime import datetime, timezone
from config import settings
from dependencies import database
import stripe
from pydantic import ValidationError

# CONFIG
router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)

security = HTTPBasic()

stripe.api_key = settings.STRIPE_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ROUTERS
@router.post("/customer-created")
async def customer_created_route(request: Request):
    try:
        response = await customer_created(request)
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail="Subscriber not created")
    except ValidationError as e:
        logger.error(f"ValidationError in customer_created_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except HTTPException as e:
        logger.error(f"HTTPException in customer_created_route: {e}")
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
    except ValueError as e:
        logger.error(f"ValueError in customer_created_route: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)  # Return an error status code, e.g., 500
    except Exception as e:
        logger.error(f"Error in customer_created_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@router.post("/subscription-updated")
async def subscription_updated_route(request: Request):
    try:
        response = await subscription_updated(request)
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail="Subscriber not created")
    except ValidationError as e:
        logger.error(f"ValidationError in subscription_updated_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except HTTPException as e:
        logger.error(f"HTTPException in subscription_updated_route: {e}")
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error(f"Error in subscription_updated_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@router.post("/subscription-deleted")
async def subscription_deleted_route(request: Request):
    try:
        response = await subscription_deleted(request)
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail="Subscriber not created")
    except ValidationError as e:
        logger.error(f"ValidationError in subscription_deleted_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except HTTPException as e:
        logger.error(f"HTTPException in subscription_deleted_route: {e}")
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error(f"Error in subscription_deleted_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

    

# FUNCTIONS
def verify_credentials(credentials: Optional[HTTPBasicCredentials] = Depends(security)) -> bool:
    correct_username = settings.SUBSCRIPTIONS_USERNAME
    correct_password = settings.SUBSCRIPTIONS_PASSWORD

    if not credentials:
        return False

    if not (secrets.compare_digest(credentials.username, correct_username) and
            secrets.compare_digest(credentials.password, correct_password)):
        return False

    return True

async def customer_created(request: Request):
    try:
        payload = await request.body()
        try:
            sig_header = request.headers["Stripe-Signature"]
        except KeyError:
            return JSONResponse(status_code=400, content={"error": "Stripe-Signature header is missing"})
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_CUSTOMER_CREATED_ENDPOINT_SECRET
        )
    except ValueError:
        # Invalid payload
        return JSONResponse(status_code=400, content={"error": "Invalid payload"})
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return JSONResponse(status_code=400, content={"error": "Invalid signature"})

    if event["type"] != "checkout.session.completed":
        return {"success": True}

    checkout_session = event["data"]["object"]

    if checkout_session["object"] != "checkout.session" or checkout_session["status"] != "complete":
        return {"success": True}

    subscriber_id = checkout_session["customer"]
    user_id = checkout_session["client_reference_id"]

    values = {
        "user_id": user_id,
        "subscriber_id": subscriber_id,
    }

    query = """
        UPDATE panda_ai_users SET subscriber_id = :subscriber_id WHERE user_id = :user_id
    """

    await database.execute(query=query, values=values)
    return JSONResponse(content={"message": "New subscriber added to database"})

async def subscription_updated(request: Request):
    try:
        payload = await request.body()
        try:
            sig_header = request.headers["Stripe-Signature"]
        except KeyError:
            return JSONResponse(status_code=400, content={"error": "Stripe-Signature header is missing"})
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SUBSCRIPTION_UPDATED_ENDPOINT_SECRET
        )
    except ValueError:
        # Invalid payload
        return JSONResponse(status_code=400, content={"error": "Invalid payload"})
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return JSONResponse(status_code=400, content={"error": "Invalid signature"})

    if event["type"] != "customer.subscription.updated":
        return {"success": True}

    subscription_updated = event["data"]["object"]

    if subscription_updated["object"] != "subscription" or subscription_updated["status"] != "active":
        return {"success": True}

    subscriber_id = subscription_updated["customer"]
    subscription_id = subscription_updated["id"]
    plan_id = subscription_updated["items"]["data"][0]["plan"]["id"]
    subscription_interval = subscription_updated["items"]["data"][0]["plan"]["interval"]

    start = subscription_updated["current_period_start"]
    end = subscription_updated["current_period_end"]
    subscription_start = datetime.fromtimestamp(start, tz=timezone.utc)
    subscription_end = datetime.fromtimestamp(end, tz=timezone.utc)
    subscription_status = subscription_updated["status"]
    
    plan_name = None
    number_messages = None
    number_integrations = None
    if plan_id in['price_1N5ZxSDrmPhl15PT1btIcShL', 'price_1N5alADrmPhl15PTFLAFBxTj', 'price_1N5ZxSDrmPhl15PTyUrmbeWI', 'price_1N5alADrmPhl15PTf8m7V3I2']:
        plan_name = "Bao"
        number_messages = 100
        number_integrations = 3
    elif plan_id in['price_1N5ZzgDrmPhl15PTlkZWtVN7', 'price_1N5akmDrmPhl15PToXSoKFUJ', 'price_1N5akmDrmPhl15PT6Rw7OYom', 'price_1N5ZzgDrmPhl15PThFxj0mfm']:
        plan_name = "Mei"
        number_messages = 300
        number_integrations = 5
    elif plan_id in['price_1N5a0sDrmPhl15PTaunA98bh', 'price_1N5akRDrmPhl15PTDgdDCmPZ', 'price_1N5a0sDrmPhl15PT8n9RF5eI', 'price_1N5akRDrmPhl15PTAek44nms']:
        plan_name = "Da"
        number_messages = 1000
        number_integrations = 99
    else:
        return JSONResponse(content={"message": "Subscription does not contain expected Plan IDs"})
    
    query1 = """
        SELECT user_id FROM panda_ai_users WHERE subscriber_id = :subscriber_id
    """
    result = await database.fetch_one(query=query1, values={"subscriber_id": subscriber_id})

    # If the result is None, the subscriber_id was not found in the table.
    if result is None:
        # Handle the error as appropriate for your application.
        raise ValueError("subscriber_id not found in panda_ai_users table")

    # Extract the user_id from the result.
    user_id = result["user_id"]


    values2 = {
        "subscriber_id": subscriber_id,
        "user_id": user_id,
        "subscription_id": subscription_id,
        "plan_id": plan_id,
        "plan_name": plan_name,
        "subscription_interval": subscription_interval,
        "subscription_start": subscription_start,
        "subscription_end": subscription_end,
        "number_messages": number_messages,
        "number_integrations": number_integrations,
        "subscription_status": subscription_status
    }

    query2 = """
        INSERT INTO panda_ai_user_subscriptions (subscriber_id, user_id, subscription_id, plan_id, plan_name, subscription_interval, subscription_start, subscription_end, number_messages, number_integrations, subscription_status)
        VALUES (:subscriber_id, :user_id, :subscription_id, :plan_id, :plan_name, :subscription_interval, :subscription_start, :subscription_end, :number_messages, :number_integrations, :subscription_status)
        ON CONFLICT (subscriber_id)
        DO UPDATE SET 
            subscription_id = excluded.subscription_id,
            user_id = excluded.user_id, 
            plan_id = excluded.plan_id, 
            plan_name = excluded.plan_name, 
            subscription_interval = excluded.subscription_interval, 
            subscription_start = excluded.subscription_start, 
            subscription_end = excluded.subscription_end, 
            number_messages = excluded.number_messages, 
            number_integrations = excluded.number_integrations;
            subscription_status = excluded.subscription_status;

    """

    await database.execute(query=query2, values=values2)


    if(subscription_end > datetime.now(timezone.utc)):
        values3 = {
            "subscriber_id": subscriber_id,
            "number_messages": number_messages,
            "number_integrations": number_integrations
        }

        query3 = """
            UPDATE panda_ai_users SET messages_per_month = :number_messages, integrations = :number_integrations WHERE subscriber_id = :subscriber_id
        """

        await database.execute(query=query3, values=values3)

    return JSONResponse(content={"message": "New subscription added to database"})

async def subscription_deleted(request: Request):
    try:
        payload = await request.body()
        try:
            sig_header = request.headers["Stripe-Signature"]
        except KeyError:
            return JSONResponse(status_code=400, content={"error": "Stripe-Signature header is missing"})
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SUBSCRIPTION_DELETED_ENDPOINT_SECRET
        )
    except ValueError:
        # Invalid payload
        return JSONResponse(status_code=400, content={"error": "Invalid payload"})
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return JSONResponse(status_code=400, content={"error": "Invalid signature"})

    if event["type"] != "customer.subscription.deleted":
        return {"success": True}

    subscription_deleted = event["data"]["object"]

    if subscription_deleted["object"] != "subscription" or subscription_deleted["status"] != "canceled":
        return {"success": True}

    subscriber_id = subscription_deleted["customer"]
    subscription_status = subscription_deleted["status"]
    plan_id = subscription_deleted["items"]["data"][0]["plan"]["id"]

    values = {
            "subscriber_id": subscriber_id,
            "plan_id": plan_id,
            "subscription_status": subscription_status
        }
    
    query = """
        UPDATE panda_ai_user_subscriptions SET subscription_status = :subscription_status WHERE subscriber_id = :subscriber_id AND plan_id = :plan_id
    """

    await database.execute(query=query, values=values)

    query2 = """
        UPDATE panda_ai_users SET messages_per_month = 0, integrations = 0 WHERE subscriber_id = :subscriber_id
    """

    await database.execute(query=query2, values={"subscriber_id": subscriber_id})

    return JSONResponse(content={"message": "Subscription cancelled"})