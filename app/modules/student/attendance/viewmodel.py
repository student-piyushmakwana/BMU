import logging
import httpx
from bs4 import BeautifulSoup
from app.core.config import config
from app.modules.student.attendance.models import AttendanceSummary, AbsentDaysData, DateAttendanceData
from typing import Optional

logger = logging.getLogger("bmu.modules.student.attendance.viewmodel")

class AttendanceError(Exception):
    """Base exception for Attendance module."""
    pass

class ExternalServiceError(AttendanceError):
    """Raised when external BMU portal fails."""
    pass

class StudentAttendanceViewModel:
    ATTENDANCE_URL = "https://bmu.gnums.co.in/StudentPanel/TTM_Attendance/TTM_Attendance_StudentAttendance.aspx"

    async def fetch_student_attendance(self, session_cookies: dict) -> AttendanceSummary:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                resp = await client.get(self.ATTENDANCE_URL)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch attendance. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise AttendanceError("Invalid session or expired cookies.")

                data = self._parse_attendance(soup)
                return AttendanceSummary(**data)

        except AttendanceError:
            raise
        except Exception as e:
            logger.error(f"Error fetching attendance: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    async def fetch_absent_days(self, session_cookies: dict, selected_semester: str) -> AbsentDaysData:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                url = f"https://bmu.gnums.co.in/StudentPanel/TTM_Attendance/TTM_Attendance_StudentAbsentDays.aspx?SelectedSemester={selected_semester}"
                resp = await client.get(url)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch absent days. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise AttendanceError("Invalid session or expired cookies.")

                data = self._parse_absent_days(soup)
                return AbsentDaysData(**data)

        except AttendanceError:
            raise
        except Exception as e:
            logger.error(f"Error fetching absent days: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    async def fetch_attendance_by_date(self, session_cookies: dict, attendance_date: str) -> DateAttendanceData:
        try:
            if not attendance_date:
                raise AttendanceError("Missing 'attendance_date' parameter.")

            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                url = (
                    "https://bmu.gnums.co.in//AdminPanel/TimeTable/TTM_Attendance/"
                    f"TTM_AttendanceViewStudentAttendanceDetailByDate.aspx?AttendanceDate={attendance_date}"
                )
                resp = await client.get(url)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch attendance by date. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise AttendanceError("Invalid session or expired cookies.")

                data = self._parse_attendance_by_date(soup, attendance_date)
                return DateAttendanceData(**data)

        except AttendanceError:
            raise
        except Exception as e:
            logger.error(f"Error fetching attendance by date: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    def _parse_attendance(self, soup: BeautifulSoup) -> dict:
        def get_text(_id):
            el = soup.find(id=_id)
            return el.get_text(strip=True) if el else None

        total_attendance = {
            "total_day": get_text("ctl00_cphPageContent_lblTotalSlots"),
            "present_day": get_text("ctl00_cphPageContent_lblTotalPresent"),
            "absent_days": get_text("ctl00_cphPageContent_lblTotalAbsent"),
            "present_percentage": get_text("ctl00_cphPageContent_lblPresentPercentage"),
        }

        semester_attendance = {
            "current_semester": get_text("ctl00_cphPageContent_rpSemesterAttendance_ctl00_lbtnSemesterAttendance"),
            "second_semester": get_text("ctl00_cphPageContent_rpSemesterAttendance_ctl01_lbtnSemesterAttendance"),
            "first_semester": get_text("ctl00_cphPageContent_rpSemesterAttendance_ctl02_lbtnSemesterAttendance"),
        }

        subjects = []
        subjects_table = soup.find("table", id="tblAttendance")
        if subjects_table:
            tbody = subjects_table.find("tbody")
            if tbody:
                for tr in tbody.find_all("tr", role="row"):
                    tds = tr.find_all("td")
                    if len(tds) < 7: continue
                    subjects.append({
                        "sr_no": tds[0].get_text(strip=True),
                        "slot_type": tds[1].get_text(strip=True),
                        "course": tds[2].get_text(strip=True),
                        "conducted": tds[3].get_text(strip=True),
                        "present": tds[4].get_text(strip=True),
                        "absent": tds[5].get_text(strip=True),
                        "attendance_percentage": tds[6].get_text(strip=True).replace("%", "").strip(),
                    })

        return {
            "semester_wise": semester_attendance,
            "total": total_attendance,
            "subjects": subjects,
        }

    def _parse_absent_days(self, soup: BeautifulSoup) -> dict:
        def get_text(_id):
            el = soup.find(id=_id)
            return el.get_text(strip=True) if el else None

        summary = {
            "partial_absent_days": get_text("ctl00_cphPageContent_lblPartialAbsentDaysCount"),
            "full_absent_days": get_text("ctl00_cphPageContent_lblFullAbsentDaysCount"),
            "total_absent_slots": get_text("ctl00_cphPageContent_lblTotalAbsentLectureLabCount"),
        }

        absents = []
        table = soup.find("table", id="tblAttendance")
        if table and table.find("tbody"):
            for tr in table.find("tbody").find_all("tr", role="row"):
                tds = tr.find_all("td")
                if len(tds) < 6: continue
                
                view_link = None
                a_tag = tds[5].find("a", href=True)
                if a_tag:
                    view_link = "https://bmu.gnums.co.in" + a_tag["href"].replace("..", "")

                absents.append({
                    "sr_no": tds[0].get_text(strip=True),
                    "attendance_date": tds[1].get_text(strip=True),
                    "conducted": tds[2].get_text(strip=True),
                    "present": tds[3].get_text(strip=True),
                    "absent": tds[4].get_text(strip=True),
                    "view_link": view_link
                })

        total = {
            "total_conducted": get_text("ctl00_cphPageContent_lblTotalConducted"),
            "total_present": get_text("ctl00_cphPageContent_lblTotalPresent"),
            "total_absent": get_text("ctl00_cphPageContent_lblTotalAbsent"),
        }

        return {
            "summary": summary,
            "absent_days": absents,
            "total": total
        }

    def _parse_attendance_by_date(self, soup: BeautifulSoup, date: str) -> dict:
        table = soup.find("table", id="tblAttendance")
        records = []
        
        if table and table.find("tbody"):
            for tr in table.find("tbody").find_all("tr", role="row"):
                tds = tr.find_all("td")
                if len(tds) < 6: continue
                records.append({
                    "sr_no": tds[0].get_text(strip=True),
                    "time": tds[1].get_text(strip=True),
                    "course": tds[2].get_text(strip=True).replace("\n", "").strip(),
                    "staff": tds[3].get_text(strip=True),
                    "slot_type": tds[4].get_text(strip=True),
                    "status": tds[5].get_text(strip=True),
                })

        total = {
            "conducted": str(len(records)),
            "present": str(sum(1 for r in records if r["status"].lower() == "present")),
            "absent": str(sum(1 for r in records if r["status"].lower() == "absent")),
        }

        return {
            "date": date,
            "records": records,
            "total": total
        }

student_attendance_viewmodel = StudentAttendanceViewModel()
