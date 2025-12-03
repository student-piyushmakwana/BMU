import logging
import httpx
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.core.config import config
from app.core.database import departments_collection
from app.modules.departments.models import InstituteDetails
from typing import Optional, Union, Dict, Any, List

logger = logging.getLogger("bmu.modules.departments.viewmodel")

class DepartmentsError(Exception):
    """Base exception for Departments module."""
    pass

class ExternalServiceError(DepartmentsError):
    """Raised when external BMU portal fails."""
    pass

class DepartmentsViewModel:
    BASE_URL = "https://bmusurat.ac.in/"

    async def get_all_departments(self) -> List[Dict[str, Any]]:
        """
        Fetch all departments from MongoDB.
        """
        try:
            cursor = departments_collection.find({"type": {"$ne": "institute_details"}})
            departments = await cursor.to_list(length=None)
            for dep in departments:
                if "_id" in dep:
                    dep["_id"] = str(dep["_id"])
            return departments
        except Exception as e:
            logger.error(f"Database error in get_all_departments: {e}", exc_info=True)
            raise DepartmentsError(f"Database error: {e}")

    async def get_department_details(self, bmu_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch department details from MongoDB by bmu_id.
        """
        try:
            try:
                bmu_id = int(bmu_id)
            except ValueError:
                pass

            doc = await departments_collection.find_one({"bmu_id": bmu_id})
            return doc
        except Exception as e:
            logger.error(f"Database error in get_department_details: {e}", exc_info=True)
            return None

    async def fetch_institute_details(self, bmu_id: int) -> InstituteDetails:
        """
        Fetch and parse institute detail page from bmusurat.ac.in for a given institute_id.
        """
        url = f"https://bmusurat.ac.in/bmu_website/institute/get_detail?institute_id={bmu_id}"

        try:
            async with httpx.AsyncClient(
                timeout=config.REQUEST_TIMEOUT,
                follow_redirects=True
            ) as client:
                resp = await client.get(url)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch institute details. Status: {resp.status_code}")

            soup = BeautifulSoup(resp.text, "html.parser")
            data = self._parse_institute_details(soup)
            return InstituteDetails(**data)

        except ExternalServiceError:
            raise
        except Exception as e:
            logger.error(f"Error fetching institute details: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")



    def _parse_institute_details(self, soup: BeautifulSoup) -> dict:
        def get_joined_text(element, separator=" "):
             if not element: return None
             return separator.join([t.strip() for t in element.find_all(text=True) if t.strip()])

        director = None
        try:
            director_div = soup.select_one("div#intellectualmember div#director")
            if director_div:
                img_tag = director_div.select_one("div.col-md-4 img")
                photo = urljoin(self.BASE_URL, img_tag["src"]) if img_tag and img_tag.get("src") else None

                name_tag = director_div.select_one("div.col-md-8 font b")
                name = name_tag.get_text(strip=True) if name_tag else None

                qualification = None
                q_bold = director_div.find("b", string=lambda s: s and "Qualification" in s)
                if q_bold:
                    texts = []
                    for sib in q_bold.parent.next_siblings:
                        if getattr(sib, "name", None) == "hr": break
                        if isinstance(sib, str) and sib.strip(): texts.append(sib.strip())
                        elif hasattr(sib, "get_text"):
                            t = sib.get_text(strip=True)
                            if t: texts.append(t)
                    qualification = ", ".join(texts).strip() or None

                email_tag = director_div.find("a", href=lambda h: h and h.startswith("mailto:"))
                email = email_tag.get_text(strip=True) if email_tag else None

                teaching_experience = None
                t_bold = director_div.find("b", string=lambda s: s and "Teaching Experience" in s)
                if t_bold:
                    texts = []
                    for sib in t_bold.parent.next_siblings:
                        if getattr(sib, "name", None) == "hr": break
                        if isinstance(sib, str) and sib.strip(): texts.append(sib.strip())
                        elif hasattr(sib, "get_text"):
                            t = sib.get_text(strip=True)
                            if t: texts.append(t)
                    teaching_experience = " ".join(texts).strip() or None

                message_p = director_div.find("p")
                message = message_p.get_text(strip=True) if message_p else None

                director = {
                    "photo": photo,
                    "name": name,
                    "qualification": qualification,
                    "email": email,
                    "teaching_experience": teaching_experience,
                    "message": message
                }
        except Exception as e:
            logger.warning(f"Director parse error: {e}")

        faculty = []
        try:
            principal_div = soup.select_one("div#intellectualmember div#principal")
            if principal_div:
                faculty_cards = principal_div.select("div.col-md-6.mb-4")
                for card in faculty_cards:
                    img = card.select_one("img")
                    photo = urljoin(self.BASE_URL, img["src"]) if img and img.get("src") else None

                    name_tag = card.select_one("font b")
                    name = name_tag.get_text(strip=True) if name_tag else None

                    designation = None
                    d_bold = card.find("b", string=lambda s: s and "Designation" in s)
                    if d_bold:
                        texts = []
                        for sib in d_bold.parent.next_siblings:
                            if getattr(sib, "name", None) == "hr": break
                            val = sib.get_text(strip=True) if hasattr(sib, "get_text") else sib.strip()
                            if val: texts.append(val)
                        designation = " ".join(texts).strip() or None

                    qual = None
                    q_label = card.find(string=lambda s: s and "Qualification" in s)
                    if q_label:
                        parent = q_label.parent
                        texts = []
                        for sib in parent.next_siblings:
                            if getattr(sib, "name", None) == "hr": break
                            val = sib.get_text(strip=True) if hasattr(sib, "get_text") else sib.strip()
                            if val: texts.append(val)
                        qual = " ".join(texts).strip() or None

                    specialization = None
                    s_bold = card.find("b", string=lambda s: s and "Specialization" in s)
                    if s_bold:
                        texts = []
                        for sib in s_bold.parent.next_siblings:
                            if getattr(sib, "name", None) == "hr": break
                            val = sib.get_text(strip=True) if hasattr(sib, "get_text") else sib.strip()
                            if val: texts.append(val)
                        specialization = " ".join(texts).strip() or None

                    email_tag = card.find("a", href=lambda h: h and h.startswith("mailto:"))
                    email = email_tag.get_text(strip=True) if email_tag else None

                    faculty.append({
                        "photo": photo,
                        "name": name,
                        "designation": designation,
                        "qualification": qual,
                        "specialization": specialization,
                        "email": email
                    })
        except Exception as e:
            logger.warning(f"Faculty parse error: {e}")

        infrastructure = []
        try:
            infra_div = soup.select_one("div#infrastructure")
            if infra_div:
                sections = infra_div.find_all("p")
                for p in sections:
                    b_tag = p.find("b")
                    if not b_tag: continue
                    title = b_tag.get_text(strip=True)
                    if not title: continue

                    images = []
                    nxt = p.find_next_sibling()
                    while nxt:
                        if nxt.name == "p": break
                        if "row" in (nxt.get("class") or []):
                            for img in nxt.find_all("img"):
                                src = img.get("src")
                                if src: images.append(urljoin(self.BASE_URL, src))
                        nxt = nxt.find_next_sibling()

                    infrastructure.append({"title": title, "images": images})
        except Exception as e:
            logger. warning(f"Infrastructure parse error: {e}")

        gallery = []
        try:
            gallery_div = soup.select_one("div#gallery")
            if gallery_div:
                titles = gallery_div.find_all("p")
                for p in titles:
                    b_tag = p.find("b")
                    if not b_tag: continue
                    title = b_tag.get_text(strip=True)
                    if not title: continue

                    images = []
                    nxt = p.find_next_sibling()
                    while nxt:
                        if nxt.name == "p": break
                        if "row" in (nxt.get("class") or []):
                            for img in nxt.find_all("img"):
                                src = img.get("src")
                                if src: images.append(urljoin(self.BASE_URL, src))
                        nxt = nxt.find_next_sibling()

                    gallery.append({"title": title, "images": images})
        except Exception as e:
            logger.warning(f"Gallery parse error: {e}")

        placement = []
        try:
            placement_div = soup.select_one("div#placement")
            if placement_div:
                members = placement_div.select("div.col-md-4")
                for m in members:
                    try:
                        img = m.find("img")
                        photo = urljoin(self.BASE_URL, img["src"]) if img else None
                        name_tag = m.find("font")
                        name = name_tag.get_text(strip=True) if name_tag else None

                        hr_parts = []
                        for seg in m.contents:
                            if hasattr(seg, "name") and seg.name == "hr": hr_parts.append("|SPLIT|")
                            else:
                                text = seg.get_text(strip=True) if hasattr(seg, "get_text") else (seg.strip() if isinstance(seg, str) else "")
                                if text: hr_parts.append(text)

                        chunks = " ".join(hr_parts).split("|SPLIT|")
                        chunks = [c.strip() for c in chunks if c.strip()]

                        qualification = chunks[1] if len(chunks) > 1 else None
                        designation = chunks[2] if len(chunks) > 2 else None
                        phone = chunks[3] if len(chunks) > 3 else None
                        email = chunks[4] if len(chunks) > 4 else None

                        phone_tag = m.find("a", href=lambda h: h and h.startswith("tel:"))
                        email_tag = m.find("a", href=lambda h: h and ("mailto" in h))
                        phone = phone_tag.get_text(strip=True) if phone_tag else phone
                        email = email_tag.get_text(strip=True) if email_tag else email

                        placement.append({
                            "photo": photo,
                            "name": name,
                            "qualification": qualification,
                            "designation": designation,
                            "phone": phone,
                            "email": email
                        })
                    except Exception as e:
                        logger.warning(f"Placement card parse error: {e}")
        except Exception as e:
            logger.warning(f"Placement parse error: {e}")

        students_recruited = []
        try:
            recruit_title = soup.find("b", string=lambda s: s and "Students Recruited" in s)
            if recruit_title:
                table = recruit_title.find_parent().find_next("table")
                if table:
                    rows = table.find_all("tr")
                    for row in rows[1:]:
                        cols = row.find_all("td")
                        if len(cols) >= 4:
                            students_recruited.append({
                                "sr_no": cols[0].get_text(strip=True),
                                "student_name": cols[1].get_text(strip=True),
                                "company_name": cols[2].get_text(strip=True),
                                "department_name": cols[3].get_text(strip=True)
                            })
        except Exception as e:
            logger.warning(f"Students Recruited parse error: {e}")

        programs = {}
        try:
            programs_div = soup.select_one("div#programs")
            if programs_div:
                tab_buttons = programs_div.select("button.subtablink")
                program_names = [btn.get_text(strip=True) for btn in tab_buttons]

                for program_name in program_names:
                    section = programs_div.find("div", id=program_name)
                    if not section: continue

                    desc_paragraphs = []
                    for p in section.find_all("p"):
                        txt = p.get_text(" ", strip=True)
                        if txt: desc_paragraphs.append(txt)

                    semesters = []
                    semester_buttons = section.select("button.accordion-btn")
                    for btn in semester_buttons:
                        sem_title = btn.get_text(strip=True)
                        panel = btn.find_next_sibling("div")
                        table = panel.find("table") if panel else None
                        subjects = []
                        if table:
                            rows = table.find_all("tr")[1:]
                            for row in rows:
                                cols = row.find_all("td")
                                if len(cols) >= 2:
                                    subjects.append({
                                        "subject_code": cols[0].get_text(strip=True),
                                        "subject_name": cols[1].get_text(strip=True)
                                    })
                        semesters.append({"semester": sem_title, "subjects": subjects})

                    programs[program_name] = {
                        "description": desc_paragraphs,
                        "semesters": semesters
                    }
        except Exception as e:
            logger.warning(f"Programs parse error: {e}")

        return {
            "director": director,
            "faculty": faculty,
            "infrastructure": infrastructure,
            "gallery": gallery,
            "placement": placement,
            "students_recruited": students_recruited,
            "programs": programs
        }

departments_viewmodel = DepartmentsViewModel()
