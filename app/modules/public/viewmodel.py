import logging
import httpx
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.core.config import config
from app.modules.public.models import PublicInfoData
from typing import Optional

logger = logging.getLogger("bmu.modules.public.viewmodel")

class PublicInfoError(Exception):
    """Base exception for Public module."""
    pass

class ExternalServiceError(PublicInfoError):
    """Raised when external BMU portal fails."""
    pass

class PublicViewModel:
    NEWS_URL = "https://bmusurat.ac.in/bmu_website/home/welcome"
    BASE_URL = "https://bmusurat.ac.in/"

    async def fetch_public_info(self) -> PublicInfoData:
        """Fetch Upcoming Events, Latest News, and Student Testimonials."""
        logger.info("Fetching public info from BMU website...")

        HEADERS = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/142.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/*,*/*;q=0.8",
            "Referer": "https://bmusurat.ac.in/",
        }

        try:
            async with httpx.AsyncClient(
                timeout=config.REQUEST_TIMEOUT,
                follow_redirects=True,
            ) as client:
                res = await client.get(self.NEWS_URL, headers=HEADERS)
                if res.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch public info. Status: {res.status_code}")

            soup = BeautifulSoup(res.text, "html.parser")
            data = self._parse_public_info(soup)
            return PublicInfoData(**data)

        except ExternalServiceError:
            raise
        except Exception as e:
            logger.error(f"Error fetching public info: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    def _parse_public_info(self, soup: BeautifulSoup) -> dict:
        results = {"upcoming_events": [], "latest_news": [], "student_testimonials": []}
        title_map = {"Upcoming Events": "upcoming_events", "Latest News": "latest_news"}

        for div in soup.find_all("div", class_="col-lg-6"):
            title = div.find("h2", class_="section-title")
            if not title: continue
            section_key = title_map.get(title.get_text(strip=True))
            if not section_key: continue

            for row in div.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) < 2: continue

                date = cols[0].get_text(strip=True)
                desc_col = cols[1]
                link_tag = desc_col.find("a")
                desc = link_tag.get_text(strip=True) if link_tag else desc_col.get_text(strip=True)
                href = link_tag.get("href") if link_tag else None
                link = urljoin(self.NEWS_URL, href) if href else None

                results[section_key].append({
                    "date": date,
                    "description": desc,
                    "link": link,
                })

        for item in soup.find_all("div", class_="testimonial-item"):
            img = item.find("img")
            name = item.find("h5")
            small = item.find("small")
            para = item.find("p")

            results["student_testimonials"].append({
                "name": name.get_text(strip=True) if name else None,
                "designation": small.get_text(strip=True) if small else None,
                "testimonial": para.get_text(strip=True) if para else None,
                "photo": urljoin(self.NEWS_URL, img.get("src")) if img else None,
            })

        return results

public_viewmodel = PublicViewModel()
