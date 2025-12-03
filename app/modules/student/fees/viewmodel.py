import re
import logging
import httpx
from bs4 import BeautifulSoup
from app.core.config import config
from app.modules.student.fees.models import FeeHistoryData, FeePostingData
from typing import Optional

logger = logging.getLogger("bmu.modules.student.fees.viewmodel")

class FeesError(Exception):
    """Base exception for Fees module."""
    pass

class ExternalServiceError(FeesError):
    """Raised when external BMU portal fails."""
    pass

class StudentFeesViewModel:
    FEE_HISTORY_URL = "https://bmu.gnums.co.in/StudentPanel/Fee/StudentFeeHistory.aspx"

    async def fetch_fee_history(self, session_cookies: dict) -> FeeHistoryData:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                resp = await client.get(self.FEE_HISTORY_URL)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch fee history. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise FeesError("Invalid session or expired cookies.")

                data = self._parse_fee_history(soup)
                return FeeHistoryData(**data)

        except FeesError:
            raise
        except Exception as e:
            logger.error(f"Error fetching fee history: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    async def fetch_fee_posting_details(self, session_cookies: dict, fee_posting_id: str) -> FeePostingData:
        try:
            if not fee_posting_id:
                raise FeesError("Missing 'fee_posting_id'.")

            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                url = f"https://bmu.gnums.co.in/StudentPanel/Fee/StudentFeeHistoryView.aspx?FeePostingID={fee_posting_id}"
                resp = await client.get(url)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch fee posting details. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise FeesError("Invalid session or expired cookies.")

                data = self._parse_fee_posting(soup)
                return FeePostingData(**data)

        except FeesError:
            raise
        except Exception as e:
            logger.error(f"Error fetching fee posting details: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    async def download_receipt(self, session_cookies: dict, receipt_id: str) -> tuple[bytes, str]:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                resp_get = await client.get(self.FEE_HISTORY_URL)
                if resp_get.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch page for receipt. Status: {resp_get.status_code}")
                
                soup = BeautifulSoup(resp_get.text, "html.parser")
                viewstate = soup.find("input", {"id": "__VIEWSTATE"})["value"]
                viewstategenerator = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})["value"]
                eventvalidation = soup.find("input", {"id": "__EVENTVALIDATION"})["value"]

                data = {
                    "__EVENTTARGET": receipt_id,
                    "__EVENTARGUMENT": "",
                    "__VIEWSTATE": viewstate,
                    "__VIEWSTATEGENERATOR": viewstategenerator,
                    "__EVENTVALIDATION": eventvalidation
                }
                
                resp_post = await client.post(self.FEE_HISTORY_URL, data=data)
                
                if resp_post.status_code != 200:
                    raise ExternalServiceError(f"Failed to download receipt. Status: {resp_post.status_code}")
                
                filename = "receipt.pdf"
                cd = resp_post.headers.get("content-disposition")
                if cd and "filename=" in cd:
                    filename = cd.split("filename=")[1].strip('"')

                return resp_post.content, filename

        except Exception as e:
            logger.error(f"Error downloading receipt: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    def _parse_fee_history(self, soup: BeautifulSoup) -> dict:
        def get_text(_id):
            el = soup.find(id=_id)
            return el.get_text(strip=True) if el else None

        fee_details = []
        main_table = soup.select_one("div#ctl00_cphPageContent_divFeePosting table.main-table")
        if main_table and main_table.find("tbody"):
            fee_rows = main_table.find("tbody").find_all("tr", recursive=False)
            for tr in fee_rows:
                tds = tr.find_all("td", recursive=False)
                if len(tds) < 11: continue

                fee_details.append({
                    "semester": tds[3].get_text(strip=True),
                    "fees_to_be_collected": tds[4].get_text(strip=True),
                    "sponsorship_amount": tds[5].get_text(strip=True),
                    "scholarship_amount": tds[6].get_text(strip=True),
                    "refunded_amount": tds[7].get_text(strip=True),
                    "previously_paid": tds[8].get_text(strip=True),
                    "paid_amount": tds[9].get_text(strip=True) if len(tds) > 9 else "0",
                    "outstanding_amount": tds[10].get_text(strip=True) if len(tds) > 10 else "0",
                    "late_fee_outstanding": "0", 
                })

        totals = {
            "total_to_be_collected": get_text("ctl00_cphPageContent_lblTotalTobeCollected"),
            "total_refunded": get_text("ctl00_cphPageContent_lblTotalAmountRefunded"),
            "total_previous_paid": get_text("ctl00_cphPageContent_lblTotalPreviousPaidAmount"),
            "total_paid": get_text("ctl00_cphPageContent_lblTotalPaidAmount"),
            "total_outstanding": get_text("ctl00_cphPageContent_lblTotalPendingAmount"),
        }

        receipts = []
        receipts_table = soup.select_one("div#ctl00_cphPageContent_divAcademicFeeReceipt table")
        if receipts_table and receipts_table.find("tbody"):
            for tr in receipts_table.find("tbody").find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) < 10: continue
                receipt_link = None
                print_btn = tds[1].find("a", href=True)
                if print_btn:
                    href = print_btn["href"]
                    if "javascript:__doPostBack" in href:
                        match = re.search(r"__doPostBack\('([^']*)'", href)
                        if match:
                            receipt_link = match.group(1)
                    else:
                        receipt_link = href

                receipts.append({
                    "sr_no": tds[0].get_text(strip=True),
                    "date": tds[2].get_text(strip=True),
                    "receipt_no": tds[3].get_text(strip=True),
                    "semester": tds[4].get_text(strip=True),
                    "payment_mode": tds[5].get_text(strip=True),
                    "ref_no": tds[6].get_text(strip=True),
                    "ref_date": tds[7].get_text(strip=True),
                    "ref_bank": tds[8].get_text(strip=True),
                    "amount": tds[9].get_text(strip=True),
                    "receipt_link": receipt_link
                })

        transactions = []
        total_transaction_amount = None
        txn_table = soup.select_one("div#ctl00_cphPageContent_Div_StudentFeePayment table")
        if txn_table and txn_table.find("tbody"):
            for tr in txn_table.find("tbody").find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) < 9: continue

                payment_details_raw = tds[7].get_text(strip=True)
                txn_split = {}
                if "Txn ID" in payment_details_raw:
                    try:
                        parts = payment_details_raw.replace("\n", "").split(",")
                        for p in parts:
                            key, value = p.split(":", 1)
                            txn_split[key.strip().lower().replace(" ", "_")] = value.strip()
                    except:
                        txn_split = {"raw": payment_details_raw}

                transactions.append({
                    "sr_no": tds[0].get_text(strip=True),
                    "payment_date": tds[1].get_text(strip=True),
                    "academic_year": tds[2].get_text(strip=True),
                    "semester": tds[3].get_text(strip=True),
                    "payment_mode": tds[4].get_text(strip=True),
                    "total_amount": tds[5].get_text(strip=True),
                    "status": tds[6].get_text(strip=True),
                    "payment_details": txn_split
                })
            
            total_transaction_amount = get_text("ctl00_cphPageContent_lblTotalFeeHeadAmount")

        return {
            "fee_data": {
                "fee_details": fee_details,
                "totals": totals
            },
            "receipts": receipts,
            "transactions": {
                "history": transactions,
                "total_transaction_amount": total_transaction_amount
            }
        }

    def _parse_fee_posting(self, soup: BeautifulSoup) -> dict:
        def get_text(_id):
            el = soup.find(id=_id)
            return el.get_text(strip=True) if el else None

        fee_plan_info = {
            "fee_plan": get_text("ctl00_cphPageContent_lblFeePlanName"),
            "fees_tobe_collected": get_text("ctl00_cphPageContent_lblAmountTotalTobeCollectedCurrency"),
            "paid_amount": get_text("ctl00_cphPageContent_lblAmountTotalPaidCurrency"),
            "academic_year": get_text("ctl00_cphPageContent_lblAcademicYearID"),
            "scholarship_amount": get_text("ctl00_cphPageContent_lblAmountTotalScholarshipCurrency"),
            "refunded_amount": get_text("ctl00_cphPageContent_lblAmountTotalRefundedCurrency"),
            "semester": get_text("ctl00_cphPageContent_lblSemester"),
            "sponsorship_amount": get_text("ctl00_cphPageContent_lblAmountTotalSponsorshipCurrency"),
            "outstanding_amount": get_text("ctl00_cphPageContent_lblAmountTotalOutStandingCurrency"),
            "fee_plan_amount": get_text("ctl00_cphPageContent_lblAmountTotalFeePlanCurrency"),
        }

        fee_heads = []
        fee_head_table = soup.select_one("table.table-bordered.table-advanced")
        if fee_head_table and fee_head_table.find("tbody"):
            for tr in fee_head_table.find("tbody").find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) < 9: continue
                fee_heads.append({
                    "sr_no": tds[0].get_text(strip=True),
                    "fee_head": tds[1].get_text(strip=True),
                    "currency": "INR", # Defaulting
                    "fee_plan_amount": "0", # Defaulting
                    "fees_tobe_collected": tds[2].get_text(strip=True),
                    "sponsorship_amount": tds[3].get_text(strip=True),
                    "scholarship_amount": tds[4].get_text(strip=True),
                    "refunded_amount": tds[5].get_text(strip=True),
                    "previously_paid": tds[6].get_text(strip=True),
                    "paid_amount": tds[7].get_text(strip=True),
                    "outstanding_amount": tds[8].get_text(strip=True),
                })

        totals = {
            "total_fee_plan_amount": get_text("ctl00_cphPageContent_lblTotalAmountFeePlanCurrency"),
            "total_fees_tobe_collected": get_text("ctl00_cphPageContent_lblTotalAmountTobeCollectedCurrency"),
            "total_scholarship_amount": get_text("ctl00_cphPageContent_lblTotalAmountScholarshipCurrency"),
            "total_sponsorship_amount": get_text("ctl00_cphPageContent_lblTotalAmountSponsorshipCurrency"),
            "total_paid_amount": get_text("ctl00_cphPageContent_lblTotalAmountPaidCurrency"),
            "total_refunded_amount": get_text("ctl00_cphPageContent_lblTotalAmountRefundedCurrency"),
            "total_outstanding_amount": get_text("ctl00_cphPageContent_lblTotalAmountOutstandingCurrency"),
        }

        return {
            "fee_plan_info": fee_plan_info,
            "fee_heads": fee_heads,
            "totals": totals
        }

student_fees_viewmodel = StudentFeesViewModel()
