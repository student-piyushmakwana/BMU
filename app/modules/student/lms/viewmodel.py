import logging
import httpx
import base64
import re
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from app.core.config import config
from app.modules.student.lms.models import LMSDashboardData, LMSSubjectData, PDFResponse
from typing import Optional

logger = logging.getLogger("bmu.modules.student.lms.viewmodel")

class LMSError(Exception):
    """Base exception for LMS module."""
    pass

class ExternalServiceError(LMSError):
    """Raised when external BMU portal fails."""
    pass

class StudentLMSViewModel:
    LMS_DASHBOARD_URL = "https://bmu.gnums.co.in/StudentPanel/LMS/LMS_ContentStudentDashboard.aspx"
    LMS_BASE_URL = "https://bmu.gnums.co.in/StudentPanel/LMS"
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "Referer": "https://bmu.gnums.co.in/StudentPanel/LMS/LMS_ContentStudentDashboard.aspx",
        "Origin": "https://bmu.gnums.co.in",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }

    async def fetch_lms_dashboard(self, session_cookies: dict, semester: Optional[str] = None) -> LMSDashboardData:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                headers=self.DEFAULT_HEADERS,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                if semester:
                    resp_get = await client.get(self.LMS_DASHBOARD_URL)
                    if resp_get.status_code != 200:
                        raise ExternalServiceError(f"Failed to fetch LMS dashboard. Status: {resp_get.status_code}")
                    
                    soup = BeautifulSoup(resp_get.text, "html.parser")
                    
                    data = {
                        tag.get("name"): tag.get("value", "")
                        for tag in soup.select("input[type=hidden]")
                        if tag.get("name")
                    }

                    data.update({
                        "__EVENTTARGET": "ctl00$cphPageHeaderRight$ddlSemester",
                        "__EVENTARGUMENT": "",
                        "ctl00$cphPageHeaderRight$ddlSemester": semester
                    })
                    
                    resp = await client.post(self.LMS_DASHBOARD_URL, data=data)
                else:
                    resp = await client.get(self.LMS_DASHBOARD_URL)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch LMS dashboard. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise LMSError("Invalid session or expired cookies.")

                data = self._parse_lms_dashboard(soup)
                return LMSDashboardData(**data)

        except LMSError:
            raise
        except Exception as e:
            logger.error(f"Error fetching LMS dashboard: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    async def fetch_lms_subject_details(self, session_cookies: dict, path: str) -> LMSSubjectData:
        try:
            if not path:
                raise LMSError("Missing 'path' parameter.")

            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            url = f"{self.LMS_BASE_URL}/{path}"
            
            async with httpx.AsyncClient(
                cookies=cookies_jar,
                headers=self.DEFAULT_HEADERS,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                resp = await client.get(url)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch subject details. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise LMSError("Invalid session or expired cookies.")

                data = self._parse_subject_details(soup, path)
                return LMSSubjectData(**data)

        except LMSError:
            raise
        except Exception as e:
            logger.error(f"Error fetching subject details: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    async def fetch_pdf_via_postback(self, session_cookies: dict, postback_id: str, form_action: str) -> PDFResponse:
        try:
            url = f"{self.LMS_BASE_URL}/{form_action}"
            
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                headers=self.DEFAULT_HEADERS,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                resp = await client.get(url)
                if resp.status_code != 200:
                     raise ExternalServiceError(f"Failed to load form for PDF. Status: {resp.status_code}")
                
                soup = BeautifulSoup(resp.text, "html.parser")

                form_data = {
                    tag.get("name"): tag.get("value", "")
                    for tag in soup.select("input[type=hidden]")
                    if tag.get("name")
                }
                form_data["__EVENTTARGET"] = postback_id
                form_data["__EVENTARGUMENT"] = ""

                post_resp = await client.post(
                    url,
                    data=form_data,
                    cookies=session_cookies,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )

                content_type = post_resp.headers.get("content-type", "").lower()
                
                if "application/pdf" in content_type or "application/download" in content_type:
                    pdf_base64 = base64.b64encode(post_resp.content).decode("utf-8")
                    return PDFResponse(pdf_base64=pdf_base64)
                else:
                    raise ExternalServiceError("PDF not returned by server.")

        except Exception as e:
            logger.error(f"Error fetching PDF: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    async def submit_rating(self, session_cookies: dict, path: str, postback_id: str) -> bool:
        try:
            url = f"{self.LMS_BASE_URL}/{path}"
            
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                headers=self.DEFAULT_HEADERS,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                resp = await client.get(url)
                if resp.status_code != 200:
                     raise ExternalServiceError(f"Failed to load page for rating. Status: {resp.status_code}")
                
                soup = BeautifulSoup(resp.text, "html.parser")

                form_data = {
                    tag.get("name"): tag.get("value", "")
                    for tag in soup.select("input[type=hidden]")
                    if tag.get("name")
                }
                
                if "__VIEWSTATE" not in form_data:
                    viewstate = soup.find("input", {"id": "__VIEWSTATE"})
                    if viewstate:
                        form_data["__VIEWSTATE"] = viewstate.get("value", "")
                
                if "__EVENTVALIDATION" not in form_data:
                    event_validation = soup.find("input", {"id": "__EVENTVALIDATION"})
                    if event_validation:
                        form_data["__EVENTVALIDATION"] = event_validation.get("value", "")

                if "__VIEWSTATEGENERATOR" not in form_data:
                    generator = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})
                    if generator:
                        form_data["__VIEWSTATEGENERATOR"] = generator.get("value", "")

                form = soup.find("form", id="aspnetForm")
                post_url = url
                if form and form.get("action"):
                    action = form.get("action")
                    if action.startswith("./"):
                        post_url = f"{self.LMS_BASE_URL}/{action[2:]}"
                    elif action.startswith("/"):
                        post_url = f"https://bmu.gnums.co.in{action}"
                    else:
                        post_url = f"{self.LMS_BASE_URL}/{action}"
                
                parsed_url = urlparse(post_url)
                query_params = parse_qs(parsed_url.query)
                for key, values in query_params.items():
                    if values:
                        form_data[key] = values[0]

                form_data["__EVENTTARGET"] = postback_id
                form_data["__EVENTARGUMENT"] = ""
                
                logger.info(f"Submitting rating to {post_url} with keys: {list(form_data.keys())}")

                post_headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": url,
                    "Origin": "https://bmu.gnums.co.in"
                }
                
                post_resp = await client.post(
                    post_url,
                    data=form_data,
                    headers=post_headers
                )

                if post_resp.status_code == 302 or (post_resp.status_code == 200 and any(r.status_code == 302 for r in post_resp.history)):
                    if "Login.aspx" in str(post_resp.url):
                        logger.error("Rating submission redirected to Login.aspx. Session likely expired or invalid.")
                        raise LMSError("Session expired or invalid. Please login again.")
                    
                    return True
                else:
                    logger.error(f"Rating submission failed. Status: {post_resp.status_code}, History: {[r.status_code for r in post_resp.history]}")
                    return False

        except Exception as e:
            logger.error(f"Error submitting rating: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    def _parse_lms_dashboard(self, soup: BeautifulSoup) -> dict:
        subjects = []
        subject_cards = soup.select("div#ctl00_cphPageContent_divSubjectWiseContentCount div.col-lg-3")

        for card in subject_cards:
            a_tag = card.find("a", href=True)
            if not a_tag: continue

            semester_span = card.select_one("span.bg-red")
            content_count_span = card.select_one("span[id$='lblCount'] b")
            subject_name_h3 = card.select_one("h3.mt-card-name")

            subjects.append({
                "subject_name": subject_name_h3.get_text(strip=True) if subject_name_h3 else None,
                "semester": semester_span.get_text(strip=True) if semester_span else None,
                "content_count": int(content_count_span.next_sibling.strip().replace(":", "")) if content_count_span else 0,
                "link": a_tag['href']
            })

        return {"subjects": subjects}

    def _parse_subject_details(self, soup: BeautifulSoup, path: str) -> dict:
        def get_text(_id):
            el = soup.find(id=_id)
            return el.get_text(strip=True) if el else None

        subject_details = {
            "subject_name": get_text("ctl00_cphPageContent_lblSubjectName"),
            "semester": get_text("ctl00_cphPageContent_lblSem"),
            "faculty": get_text("ctl00_cphPageContent_lblFaculty"),
            "course": get_text("ctl00_cphPageContent_lblCourse"),
            "base_department": get_text("ctl00_cphPageContent_lblBaseDepartment"),
            "elective": get_text("ctl00_cphPageContent_lblIsElective"),
            "common_subject": get_text("ctl00_cphPageContent_lblIsCommonSubject"),
        }

        exam_scheme = {
            "internal_theory_max": get_text("ctl00_cphPageContent_lblInternalTheoryMaxMarks"),
            "internal_theory_pass": get_text("ctl00_cphPageContent_lblInternalTheoryPassingMarks"),
            "internal_practical_max": get_text("ctl00_cphPageContent_lblInternalPracticalMaxMarks"),
            "internal_practical_pass": get_text("ctl00_cphPageContent_lblInternalPracticalPassingMarks"),
            "external_theory_max": get_text("ctl00_cphPageContent_lblExternalTheoryMaxMarks"),
            "external_theory_pass": get_text("ctl00_cphPageContent_lblExternalTheoryPassingMarks"),
            "external_practical_max": get_text("ctl00_cphPageContent_lblExternalPracticalMaxMarks"),
            "external_practical_pass": get_text("ctl00_cphPageContent_lblExternalPracticalPassingMarks"),
            "total_marks": get_text("ctl00_cphPageContent_lblTotalMark"),
            "exam_duration": get_text("ctl00_cphPageContent_lblExamDurationInMinutes")
        }

        teaching_scheme = {
            "practical_hours": get_text("ctl00_cphPageContent_lblLabHours"),
            "lecture_hours": get_text("ctl00_cphPageContent_lblLectHours"),
            "tutorial_hours": get_text("ctl00_cphPageContent_lblTutorialHours"),
            "credits": get_text("ctl00_cphPageContent_lblCredit")
        }

        syllabus_tag = soup.find(id="ctl00_cphPageContent_lbtnSyllabusPDFPath")
        syllabus_info = {
            "postback_id": syllabus_tag.get("href").split("'")[1] if syllabus_tag else None,
            "form_action": path,
            "title": syllabus_tag.get("title") if syllabus_tag else "Syllabus PDF"
        } if syllabus_tag else None

        staff_details = None
        staff_div = soup.find("div", id="ctl00_cphPageContent_rpSubjectInstructorDetails_ctl00_divStaff")
        
        staff_name_span = soup.find("span", id=lambda x: x and "lblStaffFullName" in x)
        if staff_name_span:
            staff_container = staff_name_span.find_parent("div", class_="col-lg-10")
            img_tag = soup.find("img", id=lambda x: x and "imgUser" in x)
            designation_span = soup.find("span", id=lambda x: x and "lblDesignationName" in x)
            email_a = staff_container.find("a", href=lambda x: x and "mailto:" in x) if staff_container else None

            staff_details = {
                "name": staff_name_span.get_text(strip=True),
                "designation": designation_span.get_text(strip=True) if designation_span else None,
                "email": email_a.get_text(strip=True) if email_a else None,
                "image_url": img_tag["src"].replace("../../", "https://bmu.gnums.co.in/") if img_tag else None
            }

        units = []
        unit_table = soup.select_one("div[id$='divSubjectWiseUnit'] table")
        if unit_table and unit_table.find("tbody"):
            for tr in unit_table.find("tbody").find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) >= 4:
                    units.append({
                        "sr_no": tds[0].get_text(strip=True),
                        "unit_name": tds[1].get_text(strip=True).rstrip(":"),
                        "weightage": tds[2].get_text(strip=True),
                        "teaching_hours": tds[3].get_text(strip=True)
                    })

        content_categories = []
        tabs_ul = soup.select_one("div.tabbable-line ul.nav-tabs")
        if tabs_ul:
            for li in tabs_ul.find_all("li"):
                a_tag = li.find("a")
                if not a_tag: continue
                
                category_name = a_tag.get_text(strip=True)
                count_span = a_tag.find("span", class_="badge")
                count = 0
                if count_span:
                    count = int(count_span.get_text(strip=True))
                    category_name = category_name.replace(count_span.get_text(strip=True), "").strip()
                
                tab_id = a_tag["href"].replace("#", "")
                
                items = []
                tab_pane = soup.find("div", id=tab_id)
                if tab_pane:
                    content_table = tab_pane.find("table")
                    if content_table and content_table.find("tbody"):
                        for tr in content_table.find("tbody").find_all("tr"):
                            if tr.find("th"): continue
                            
                            tds = tr.find_all("td")
                            if len(tds) < 6: continue

                            title_a = tds[1].find("a")
                            title = title_a.get_text(strip=True) if title_a else ""
                            link = title_a["href"] if title_a else None

                            download_a = tds[2].find("a", id=lambda x: x and "hlDocumentPath" in x)
                            
                            date_text = tds[3].get_text(strip=True)
                            updated_date = date_text[:10] if len(date_text) >= 10 else date_text
                            updated_time = tds[3].find("small").get_text(strip=True) if tds[3].find("small") else ""

                            rating_data = None
                            if len(tds) >= 7:
                                rating_cell = tds[6]
                                rating_small = rating_cell.find("small")
                                current_rating = rating_small.get_text(strip=True) if rating_small else None
                                
                                options = []
                                star_links = rating_cell.find_all("a", href=lambda x: x and "javascript:__doPostBack" in x)
                                for idx, star_link in enumerate(star_links):
                                    href = star_link.get("href", "")
                                    match = re.search(r"__doPostBack\('([^']*)'", href)
                                    if match:
                                        options.append({
                                            "star_value": idx + 1,
                                            "postback_id": match.group(1)
                                        })
                                
                                if current_rating or options:
                                    rating_data = {
                                        "current_rating": current_rating,
                                        "options": options
                                    }

                            items.append({
                                "sr_no": tds[0].get_text(strip=True),
                                "title": title,
                                "link": link,
                                "download_link": download_a["href"].replace("../../", "https://bmu.gnums.co.in/") if download_a else None,
                                "updated_date": updated_date,
                                "updated_time": updated_time,
                                "prepared_by": tds[4].get_text(strip=True),
                                "view_status": tds[5].get_text(strip=True),
                                "rating": rating_data
                            })

                content_categories.append({
                    "category_name": category_name,
                    "count": count,
                    "items": items
                })

        return {
            "subject_details": subject_details,
            "syllabus": syllabus_info,
            "staff_details": staff_details,
            "exam_scheme": exam_scheme,
            "teaching_scheme": teaching_scheme,
            "units": units,
            "content_categories": content_categories
        }

student_lms_viewmodel = StudentLMSViewModel()
