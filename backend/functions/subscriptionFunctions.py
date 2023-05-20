from fastapi import HTTPException
from config import settings
from databases import Database
from pydantic import ValidationError
import stripe, logging

# DATABASES
DATABASE_URL = settings.PSQL_DATABASE_URL
database = Database(DATABASE_URL)

stripe_api_key = settings.STRIPE_API_KEY


# SUBSCRIPTION FUNCTIONS
async def get_user_messages_this_month(user_id: str):
    query = "SELECT COUNT(*) AS count FROM panda_ai_messages WHERE user_id = :user_id AND success = true AND EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM NOW()) AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW())"
    values = {"user_id": user_id}
    result = await database.fetch_one(query=query, values=values)

    return result

async def get_subscriber_and_user_messages_per_month(user_id: str):
    query = "SELECT subscriber, messages_per_month FROM panda_ai_users WHERE user_id = :user_id"
    values = {"user_id": user_id}
    result = await database.fetch_one(query=query, values=values)

    return result

async def cancel_subscription(user_id: str):
    query = "SELECT subscription_id FROM panda_ai_user_subscriptions WHERE user_id = :user_id"
    values = {"user_id": user_id}
    try:
        result = await database.fetch_one(query=query, values=values)

        if result:
            try:
                stripe.Subscription.delete(
                    result['subscription_id'],
                )
                logging.info(f"Subscription {result['subscription_id']} for user {user_id} cancelled successfully")
                return {"message": "Subscription cancelled successfully"}
            except Exception as e:
                logging.error(f"Exception while cancelling subscription for user {user_id} on Stripe: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        else:
            logging.info(f"No subscription found for user {user_id}")
            return {"message": "No subscription found for user"}

    except ValidationError as e:
        response = {"error": "Validation error", "details": e.errors()}
        logging.error(f"Validation error while cancelling subscription for user {user_id}: {response}")
        return response

    except Exception as e:
        response = {"error": str(e)}
        logging.error(f"Exception while cancelling subscription for user {user_id}: {str(e)}")
        return response
