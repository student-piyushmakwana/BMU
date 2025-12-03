import logging
import httpx
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.core.config import config
from app.modules.student.timetable.models import TimetableData
from typing import Optional

logger = logging.getLogger("bmu.modules.student.timetable.viewmodel")

class TimetableError(Exception):
    """Base exception for Timetable module."""
    pass

class ExternalServiceError(TimetableError):
    """Raised when external BMU portal fails."""
    pass

class StudentTimetableViewModel:
    BASE_URL = "https://bmu.gnums.co.in/Login.aspx"
    TIMETABLE_URL = "StudentPanel/TTM_TimeTable/TTM_TimeTable_StudentTimeTable.aspx"

    async def fetch_student_timetable(self, session_cookies: dict, timetable_date: Optional[str] = None) -> TimetableData:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            url = urljoin(self.BASE_URL, self.TIMETABLE_URL)
            
            async with httpx.AsyncClient(
                cookies=cookies_jar,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                resp = await client.get(url)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch timetable page. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise TimetableError("Invalid session or expired cookies.")

                if timetable_date:
                    form_data = {
                        tag.get("name"): tag.get("value", "")
                        for tag in soup.select("input[type=hidden]")
                        if tag.get("name")
                    }
                    
                    form_data.update({
                        "__EVENTTARGET": "ctl00$cphPageContent$dtpTimeTableAsOn",
                        "__EVENTARGUMENT": "",
                        "ctl00$cphPageContent$dtpTimeTableAsOn": timetable_date
                    })

                    if "ctl00$cphPageContent$sm" in form_data:
                        form_data["ctl00$cphPageContent$sm"] = "ctl00$cphPageContent$upTTM_Attendance|ctl00$cphPageContent$dtpTimeTableAsOn"

                    post_resp = await client.post(
                        url,
                        data=form_data,
                        headers={"Content-Type": "application/x-www-form-urlencoded"}
                    )
                    
                    if post_resp.status_code == 500:
                        logger.warning(f"Server 500 error for date {timetable_date}, using default timetable.")
                    elif post_resp.status_code == 200:
                        soup = BeautifulSoup(post_resp.text, "html.parser")
                    else:
                        raise ExternalServiceError(f"Failed to fetch timetable for date {timetable_date}. Status: {post_resp.status_code}")

                data = self._parse_timetable(soup)
                return TimetableData(**data)

        except TimetableError:
            raise
        except Exception as e:
            logger.error(f"Error fetching timetable: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    def _parse_timetable(self, soup: BeautifulSoup) -> dict:
        table = soup.find("table", {"id": "sample_1"})
        if not table:
             raise TimetableError("Timetable table not found.")

        headers = [th.get_text(separator=" ", strip=True) for th in table.find_all("th")]
        days = headers[1:]

        timetable = []
        rows = table.find_all("tr")[1:]

        for row in rows:
            cols = row.find_all("td")
            if not cols: continue

            time_slot = cols[0].get_text(separator=" ", strip=True)
            day_entries = []

            for day_index, col in enumerate(cols[1:], start=1):
                lectures = []
                blocks = [b for b in col.decode_contents().split("<hr") if b.strip()]

                for block in blocks:
                    temp = BeautifulSoup(block, "html.parser")
                    lines = [t.get_text(strip=True) for t in temp.find_all(text=True) if t.strip()]
                    if not lines: continue

                    batch, subject, faculty, room = "", "", "", ""
                    for line in lines:
                        if "Batch" in line or 'style="margin:5px;padding:0px;' in line:
                            batch = line.replace('style="margin:5px;padding:0px;"/>', "").strip()
                        elif line.startswith("{"):
                            faculty = line.strip("{}").strip()
                        elif line.startswith("["):
                            room = line.strip()
                        else:
                            subject = line.strip()

                    lectures.append({
                        "batch": batch,
                        "subject": subject.replace(" - ", "-"),
                        "faculty": faculty,
                        "room": room,
                    })

                day_entries.append({
                    "day": days[day_index - 1],
                    "lectures": lectures
                })

            timetable.append({
                "time_slot": time_slot,
                "schedule": day_entries
            })

        header_label = soup.find("label", {"id": "lblTimeTable"})
        header_text = header_label.get_text(separator=" ", strip=True) if header_label else ""

        date_label = soup.find("label", {"id": "lblDate"})
        effective_from = date_label.get_text(strip=True).replace("w.e.f.", "").strip() if date_label else None

        return {
            "institute": "Bhagwan Mahavir College of Management",
            "class_info": header_text,
            "effective_from": effective_from,
            "timetable": timetable
        }

student_timetable_viewmodel = StudentTimetableViewModel()
