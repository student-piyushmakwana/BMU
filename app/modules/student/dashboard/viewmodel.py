import logging
import httpx
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.modules.student.dashboard.models import DashboardData
from typing import Optional

logger = logging.getLogger("bmu.modules.student.dashboard.viewmodel")

class DashboardError(Exception):
    """Base exception for Dashboard module."""
    pass

class ExternalServiceError(DashboardError):
    """Raised when external BMU portal fails."""
    pass

class StudentDashboardViewModel:
    DASHBOARD_URL = "https://bmu.gnums.co.in/StudentPanel/StudentDashboard.aspx"

    async def fetch_student_dashboard(self, session_cookies: dict) -> DashboardData:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(cookies=cookies_jar, follow_redirects=True) as client:
                resp = await client.get(self.DASHBOARD_URL)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch dashboard. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")

                if soup.find("input", {"id": "txtUsername"}):
                    raise DashboardError("Invalid session or expired cookies.")

                data = self._parse_dashboard(soup)
                return DashboardData(**data)

        except DashboardError:
            raise
        except Exception as e:
            logger.error(f"Error fetching dashboard: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    def _parse_dashboard(self, soup: BeautifulSoup) -> dict:
        def get_text(_id):
            el = soup.find(id=_id)
            return el.text.strip() if el else None

        def get_img(_id):
            img = soup.find(id=_id)
            if not img: return None
            src = img.get("src")
            return src if src.startswith("data:image") else urljoin(self.DASHBOARD_URL, src)
        
        def clean_value(val, remove_brackets=False):
            import re
            if val is None: return None
            if isinstance(val, str):
                val = val.replace("|", "").strip()
                if remove_brackets:
                    val = re.sub(r"[\(\)]", "", val).strip()
                return val if val else None
            return val

        def transform_gender(val):
            if val is None: return None
            val = val.strip().upper()
            mapping = {"M": "Male", "F": "Female"}
            return mapping.get(val, val)

        data = {
            "personal": {
                "full_name": clean_value(get_text("ctl00_lblCurrentUsername") or get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblStudentLCName")),
                "profile_image_main": clean_value(get_img("ctl00_imgCurrentUserPhoto")),
                "profile_image_responsive": clean_value(get_img("ctl00_cphPageContent_ucStudentInfoCompact_imgStudentPhoto")),
                "birth_date": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblBirthDate")),
                "gender": transform_gender(clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblGender"))),
            },
            "education": {
                "course_name": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblCourseName")),
                "semester": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblCurrentSemester"), remove_brackets=True),
                "enrollment_no": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblEnrollmentNo")),
                "abc_id": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblABCID")),
                "status": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblStudentStatusID")),
                "division": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblCurrentDivision")),
                "batch_no": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblCurrentLabBatchNo")),
                "roll_no": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblCurrentRollNo")),
            },
            "contact": {
                "mobile_no": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblPhoneStudent1") or get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblPhoneStudent2")),
                "email": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblEmail") or get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblEmailAlternate")),
            },
            "family": {
                "father_name": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblFatherName")),
                "father_mobile": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblFatherMobile")),
                "mother_name": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblMotherName")),
                "mother_mobile": clean_value(get_text("ctl00_cphPageContent_ucStudentInfoCompact_lblMotherMobile")),
            },
            "pending_assignments": []
        }

        try:
            assignments_div = soup.find("div", id="ctl00_cphPageContent_divPendingAssigmnets")
            if assignments_div:
                table = assignments_div.find("table")
                if table:
                    rows = table.find_all("tr")[1:]
                    for row in rows:
                        cols = row.find_all("td")
                        if len(cols) >= 5:
                            data["pending_assignments"].append({
                                "sr_no": cols[0].get_text(strip=True),
                                "subject": cols[1].get_text(strip=True),
                                "assignment_name": cols[2].find("a").get_text(strip=True) if cols[2].find("a") else None,
                                "last_date": cols[3].get_text(" ", strip=True)
                            })
        except Exception as e:
            logger.warning(f"Failed to parse pending assignments: {e}")

        return data

student_dashboard_viewmodel = StudentDashboardViewModel()
