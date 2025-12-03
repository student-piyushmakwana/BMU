import motor.motor_asyncio as motor
from app.core.config import config


class Database:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = motor.AsyncIOMotorClient(config.MONGO_URI)
        return cls._instance


def get_db():
    client = Database.get_instance()
    return client["BMU"]


db = get_db()
departments_collection = db["Departments"]
users_collection = db["Users"]
