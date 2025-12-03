import logging
import asyncio
import httpx
from app.core.client import BMUClient
from app.core.config import config
from app.modules.auth.models import AuthModel

logger = logging.getLogger("bmu.modules.auth.viewmodel")

class AuthError(Exception):
    """Base exception for Auth module."""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(message)

class AuthenticationError(AuthError):
    """Raised when authentication fails."""
    pass

class ExternalServiceError(AuthError):
    """Raised when external BMU portal fails."""
    pass

class AuthViewModel:
    BASE_URL = "https://bmu.gnums.co.in/Login.aspx"

    async def _get_initial_login_page(self):
        client = BMUClient.get_client()
        try:
            response = await client.get(self.BASE_URL)
            response.raise_for_status()

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            def val(_id):
                el = soup.find("input", {"id": _id})
                return el.get("value", "") if el else ""

            login_state = {
                "__VIEWSTATE": val("__VIEWSTATE"),
                "__EVENTVALIDATION": val("__EVENTVALIDATION"),
                "__VIEWSTATEGENERATOR": val("__VIEWSTATEGENERATOR"),
                "__VIEWSTATEENCRYPTED": val("__VIEWSTATEENCRYPTED"),
                "hfWidth": val("hfWidth"),
                "hfHeight": val("hfHeight"),
                "hfLoginMethod": val("hfLoginMethod"),
            }

            if not login_state["__VIEWSTATE"]:
                raise ExternalServiceError("Failed to parse login page fields.")

            return login_state

        except Exception as e:
            logger.error(f"Error fetching login page: {e}", exc_info=True)
            if isinstance(e, ExternalServiceError):
                raise
            raise ExternalServiceError(f"Failed to load login page: {e}")

    async def login_with_credentials(self, username: str, password: str, retries: int = 3, backoff: float = 2.0):
        logger.info(f"Attempting login for user: {username}")
        client = BMUClient.get_client()

        try:
            login_state = await self._get_initial_login_page()
            
            payload = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATE": login_state.get("__VIEWSTATE", ""),
                "__VIEWSTATEGENERATOR": login_state.get("__VIEWSTATEGENERATOR", ""),
                "__EVENTVALIDATION": login_state.get("__EVENTVALIDATION", ""),
                "__VIEWSTATEENCRYPTED": login_state.get("__VIEWSTATEENCRYPTED", ""),
                "hfWidth": login_state.get("hfWidth", ""),
                "hfHeight": login_state.get("hfHeight", ""),
                "hfLoginMethod": login_state.get("hfLoginMethod", ""),
                "rblRole": "Student",
                "txtUsername": username,
                "txtPassword": password,
                "btnLogin": "Login",
            }

            for attempt in range(1, retries + 1):
                try:
                    client.follow_redirects = False
                    response = await client.post(self.BASE_URL, data=payload, timeout=config.REQUEST_TIMEOUT)
                    client.follow_redirects = True

                    if response.status_code == 302:
                        location = response.headers.get("Location", "")
                        if any(x in location for x in ["Default.aspx", "StudentPanel/StudentDashboard.aspx"]):
                            return {
                                "session_cookies": dict(client.cookies),
                            }
                        raise AuthenticationError(f"Unexpected redirect: {location}")

                    if response.status_code == 200:
                        raise AuthenticationError("Invalid username or password.")

                    response.raise_for_status()

                except (httpx.ConnectError, httpx.NetworkError) as e:
                    if attempt < retries:
                        await asyncio.sleep(backoff * attempt)
                        continue
                    raise ExternalServiceError(f"Network error after {retries} attempts: {e}")
                except httpx.TimeoutException as e:
                    if attempt < retries:
                        await asyncio.sleep(backoff * attempt)
                        continue
                    raise ExternalServiceError(f"Timeout after {retries} attempts: {e}")

        except AuthError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    async def check_student_session(self, session_cookies: dict) -> bool:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(cookies=cookies_jar, follow_redirects=True) as client:
                DASHBOARD_URL = "https://bmu.gnums.co.in/StudentPanel/StudentDashboard.aspx"
                resp = await client.get(DASHBOARD_URL)
                
                if resp.status_code != 200:
                    return False

                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, "html.parser")
                if soup.find("input", {"id": "txtUsername"}):
                    return False

            return True

        except Exception as e:
            logger.warning(f"Session check failed: {e}")
            return False

    async def google_login(self, google_id: str, username: str = None, password: str = None):
        try:
            if username and password:
                await self.login_with_credentials(username, password)

                existing_user = await AuthModel.find_user_by_username(username)
                if existing_user and existing_user.get("google_id") != google_id:
                    raise AuthError("This BMU account is already linked to another Google account.", code="ACCOUNT_ALREADY_LINKED")
                
                await AuthModel.update_user_credentials(google_id, username, password)
                
                return await self.login_with_credentials(username, password)

            user = await AuthModel.find_user_by_google_id(google_id)
            
            if not user:
                await AuthModel.create_user({
                    "google_id": google_id,
                    "username": None,
                    "password": None
                })
                raise AuthError("Account created. Please link your BMU account.", code="ACCOUNT_CREATED_NEEDS_LINKING")

            stored_username = user.get("username")
            stored_password = user.get("password")

            if not stored_username or not stored_password:
                raise AuthError("Account exists but is not linked to BMU credentials.", code="ACCOUNT_NEEDS_LINKING")

            return await self.login_with_credentials(stored_username, stored_password)

        except AuthError:
            raise
        except Exception as e:
            logger.error(f"Google login error: {e}", exc_info=True)
            raise ExternalServiceError(f"Google login failed: {e}")

    async def logout(self, session_cookies: dict):
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(cookies=cookies_jar, follow_redirects=True) as client:
                DASHBOARD_URL = "https://bmu.gnums.co.in/StudentPanel/StudentDashboard.aspx"
                response = await client.get(DASHBOARD_URL)
                
                if "Login.aspx" in str(response.url):
                     raise AuthenticationError("Session invalid or expired.")

                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, "html.parser")

                def val(_id):
                    el = soup.find("input", {"id": _id})
                    return el.get("value", "") if el else ""

                payload = {
                    "__EVENTTARGET": "ctl00$lbtnLogout",
                    "__EVENTARGUMENT": "",
                    "__VIEWSTATE": val("__VIEWSTATE"),
                    "__VIEWSTATEGENERATOR": val("__VIEWSTATEGENERATOR"),
                    "__EVENTVALIDATION": val("__EVENTVALIDATION"),
                    "__VIEWSTATEENCRYPTED": val("__VIEWSTATEENCRYPTED"),
                    "hfWidth": val("hfWidth"),
                    "hfHeight": val("hfHeight"),
                    "hfLoginMethod": val("hfLoginMethod"),
                }

                logout_response = await client.post(DASHBOARD_URL, data=payload)
                
                if "Login.aspx" in str(logout_response.url):
                     return True
                
                raise ExternalServiceError("Logout failed. Could not verify redirection.")

        except AuthError:
            raise
        except Exception as e:
            logger.error(f"Logout error: {e}", exc_info=True)
            raise ExternalServiceError(f"Logout failed: {e}")

auth_viewmodel = AuthViewModel()
