import os
import secrets
import logging
import urllib.parse as parser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("bmu.config")
logger.info("⚙️ Initializing BMU API configuration...")


class Config:
    """Base configuration class (shared across all environments)."""

    SECRET_KEY = os.environ.get("BMU_SECRET_KEY") or secrets.token_urlsafe(32)

    DB_USER = parser.quote_plus(os.environ.get('DB_USER'))
    DB_PASSWORD = parser.quote_plus(os.environ.get('DB_PASSWORD'))
    DB_CLUSTER = os.environ.get('DB_CLUSTER')
    MONGO_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true"

    REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", 20))

    PROJECT_NAME = "BMU API"
    DEVELOPER = "Piyush Makwana"

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    APP_ENV = os.environ.get("APP_ENV", "production").lower()
    EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL") or os.environ.get("EXTERNAL_URL")

    def __init__(self):
        logger.debug("Base Config initialized.")
        logger.debug(f"REQUEST_TIMEOUT = {self.REQUEST_TIMEOUT}s")


class DevelopmentConfig(Config):
    """Configuration for local development."""
    DEBUG = True

    def __init__(self):
        super().__init__()
        logger.info("💻 Using Development Configuration")


class ProductionConfig(Config):
    """Configuration for production."""
    DEBUG = False

    def __init__(self):
        super().__init__()
        logger.info("🏭 Using Production Configuration")


ENVIRONMENT = os.environ.get("APP_ENV", "production").lower()

if ENVIRONMENT == "development":
    config = DevelopmentConfig()
else:
    config = ProductionConfig()

logger.info(f"✅ Active configuration: {config.__class__.__name__}")
logger.info(f"🧠 Log level: {LOG_LEVEL}")
logger.info(f"⏱ Request timeout: {config.REQUEST_TIMEOUT}s")
