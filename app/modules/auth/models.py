from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.core.database import users_collection
import logging

logger = logging.getLogger("bmu.modules.auth.models")

class LoginRequest(BaseModel):
    username: str
    password: str

class GoogleLoginRequest(BaseModel):
    google_id: str
    username: Optional[str] = None
    password: Optional[str] = None

class SessionCheckRequest(BaseModel):
    session_cookies: Dict[str, str]

class User(BaseModel):
    google_id: str
    username: Optional[str]
    password: Optional[str]

class AuthModel:
    @staticmethod
    async def find_user_by_google_id(google_id: str) -> Optional[Dict[str, Any]]:
        try:
            return await users_collection.find_one({"google_id": google_id})
        except Exception as e:
            logger.error(f"Error finding user by google_id: {e}", exc_info=True)
            raise

    @staticmethod
    async def find_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        try:
            return await users_collection.find_one({"username": username})
        except Exception as e:
            logger.error(f"Error finding user by username: {e}", exc_info=True)
            raise

    @staticmethod
    async def create_user(user_data: Dict[str, Any]):
        try:
            await users_collection.insert_one(user_data)
        except Exception as e:
            logger.error(f"Error creating user: {e}", exc_info=True)
            raise

    @staticmethod
    async def update_user_credentials(google_id: str, username: str, password: str):
        try:
            await users_collection.replace_one(
                {"google_id": google_id},
                {
                    "google_id": google_id,
                    "username": username,
                    "password": password
                },
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error updating user credentials: {e}", exc_info=True)
            raise
