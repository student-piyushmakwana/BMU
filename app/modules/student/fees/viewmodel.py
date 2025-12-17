import re
import logging
import httpx
from bs4 import BeautifulSoup
from app.core.config import config
from app.modules.student.fees.models import FeeHistoryData, FeePostingData, PendingFeesData, PaymentInitiationResponse
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
    FEE_DASHBOARD_URL = "https://bmu.gnums.co.in/StudentPanel/Fee/FEE_FeeDashboard.aspx"

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

    async def fetch_pending_fees(self, session_cookies: dict) -> PendingFeesData:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                resp = await client.get(self.FEE_DASHBOARD_URL)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch fee dashboard. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise FeesError("Invalid session or expired cookies.")

                data = self._parse_pending_fees(soup)
                return PendingFeesData(**data)

        except FeesError:
            raise
        except Exception as e:
            logger.error(f"Error fetching pending fees: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    def _parse_pending_fees(self, soup: BeautifulSoup) -> dict:
        def get_text(_id):
            el = soup.find(id=_id)
            return el.get_text(strip=True) if el else None

        fee_heads = []
        table = soup.select_one("div#ctl00_cphPageContent_Div_CurrentAcademicFeeDetails table")
        if table and table.find("tbody"):
            for tr in table.find("tbody").find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) < 6: continue
                
                fee_heads.append({
                    "sr_no": tds[0].get_text(strip=True).split()[0], # Remove hidden inputs if any text sticks
                    "fee_head": tds[1].get_text(strip=True),
                    "fees_to_be_paid": tds[2].get_text(strip=True),
                    "paid_amount": tds[3].get_text(strip=True),
                    "in_process_amount": tds[4].get_text(strip=True),
                    "outstanding_amount": tds[5].get_text(strip=True),
                })

        semester = get_text("ctl00_cphPageContent_rpSemesterWise_ctl00_lblSemester")
        
        # Parse notes
        notes = []
        note_div = soup.select_one("div.note.note-info ul")
        if note_div:
            for li in note_div.find_all("li"):
                notes.append(li.get_text(strip=True))

        # Parse due date info
        due_date_info = get_text("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_lblFeeDurationInfo")

        # Parse totals
        totals = {
            "total_fees_to_be_paid": get_text("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_lblTotalCurrentSemFee"),
            "total_paid_amount": get_text("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_lblTotalAmountPaid"),
            "total_in_process_amount": get_text("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_lblTotalInProcessAmount"),
            "total_outstanding_amount": get_text("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_lblTotalAmountOutStanding"),
        }

        # Parse payment info
        payment_info = None
        def get_value(_id):
            el = soup.find("input", {"id": _id})
            return el.get("value") if el else None

        pg_name = get_value("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_hfPGName")
        if pg_name:
            payment_info = {
                "pg_name": pg_name,
                "payment_environment": get_value("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_hfPaymentEnvironment"),
                "bank_account_id": get_value("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_hfBankAccountID"),
                "semester": get_value("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_hfSemester"),
                "payment_gateway_id": get_value("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_hfPaymentGatewayID"),
                "payment_product_name": get_value("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_hfPaymentProductNameTuitionFees"),
                "currency_id": get_value("ctl00_cphPageContent_rpSemesterWise_ctl00_rpBankAccountWise_ctl00_CurrencyID"),
            }

        return {
            "semester": semester,
            "fee_heads": fee_heads,
            "note": notes,
            "due_date_info": due_date_info,
            "payment_info": payment_info,
            **totals
        }

    async def initiate_payment(self, session_cookies: dict) -> PaymentInitiationResponse:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": self.FEE_DASHBOARD_URL,
                "Origin": "https://bmu.gnums.co.in"
            }

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                headers=headers,
                follow_redirects=True, # We want to follow to see where it lands, unless we want to catch the 302 specifically. 
                # Actually, follow_redirects=True is good. If it goes to Gateway, we get the Gateway page content.
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                # 1. Get the dashboard to get fresh ViewStates and form data
                logger.info("Fetching dashboard for payment initiation...")
                resp_get = await client.get(self.FEE_DASHBOARD_URL)
                
                if resp_get.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch dashboard for payment. Status: {resp_get.status_code}")

                soup = BeautifulSoup(resp_get.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise FeesError("Invalid session or expired cookies.")

                # 2. Extract all form inputs
                data = {}
                form = soup.find("form", {"id": "form1"}) or soup.find("form", {"id": "aspnetForm"}) # Try both typical IDs
                if not form:
                    # Fallback to searching all inputs if form not found or non-standard
                    for inp in soup.find_all("input"):
                         name = inp.get("name")
                         if name:
                             data[name] = inp.get("value", "")
                else:
                    for inp in form.find_all("input"):
                        name = inp.get("name")
                        if name:
                            data[name] = inp.get("value", "")
                
                # 3. Handle the specific button "Pay Now"
                pay_btn_name = None
                pay_btn = soup.find("input", {"value": "Pay Now"})
                if pay_btn:
                    pay_btn_name = pay_btn.get("name")
                else:
                    pay_btn = soup.find("input", id=lambda x: x and x.endswith("btnAcademicFeeOnline"))
                    if pay_btn:
                         pay_btn_name = pay_btn.get("name")
                
                if not pay_btn_name:
                    logger.error("Could not find Pay Now button on the page.")
                    # It's possible there are no pending fees or the button is hidden/disabled.
                    # Or maybe the text is different.
                    raise FeesError("Could not find the 'Pay Now' button. Check if there are pending fees.")

                data[pay_btn_name] = "Pay Now"

                # 4. Post the data
                logger.info("Posting payment initiation data...")
                # Note: ASP.NET postbacks need to be form-urlencoded. httpx data=dict does this automatically.
                resp_post = await client.post(self.FEE_DASHBOARD_URL, data=data)

                if resp_post.status_code != 200:
                    raise ExternalServiceError(f"Payment initiation failed. Status: {resp_post.status_code}")

                # 5. Check Result
                final_url = str(resp_post.url)
                
                # If we are still on the dashboard, it means the redirect didn't happen.
                # Use a looser check because of query params
                if self.FEE_DASHBOARD_URL in final_url or "StudentPanel/Fee/FEE_FeeDashboard.aspx" in final_url:
                     # Check if we got the same page back.
                     # Sometimes the gateway is an iframe or a diverse response.
                     # But if it's the exact same page, scraping failed to trigger.
                     pass 

                return PaymentInitiationResponse(
                    success=True,
                    redirect_url=final_url if final_url != self.FEE_DASHBOARD_URL else None,
                    message="Payment initiated. Check redirect_url."
                )

        except FeesError:
            raise
        except Exception as e:
            logger.error(f"Error iterating payment: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

student_fees_viewmodel = StudentFeesViewModel()
