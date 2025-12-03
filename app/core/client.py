import httpx
import logging
from app.core.config import config

logger = logging.getLogger("bmu.core.client")

class BMUClient:
    _instance = None

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            logger.info("Initializing shared HTTP client...")
            cls._instance = httpx.AsyncClient(
                timeout=config.REQUEST_TIMEOUT,
                follow_redirects=True,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/142.0.0.0 Safari/537.36"
                    ),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/*,*/*;q=0.8",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "Referer": "https://bmu.gnums.co.in/Login.aspx",
                    "Origin": "https://bmu.gnums.co.in",
                },
            )
        return cls._instance

    @classmethod
    async def close_client(cls):
        if cls._instance:
            await cls._instance.aclose()
            cls._instance = None
            logger.info("Shared HTTP client closed.")
