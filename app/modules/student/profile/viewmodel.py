import logging
import httpx
from bs4 import BeautifulSoup
from app.core.config import config
from app.core.utils import clean_labelled_text
from app.modules.student.profile.models import ProfileData
from typing import Optional

logger = logging.getLogger("bmu.modules.student.profile.viewmodel")

class ProfileError(Exception):
    """Base exception for Profile module."""
    pass

class ExternalServiceError(ProfileError):
    """Raised when external BMU portal fails."""
    pass

class StudentProfileViewModel:
    PROFILE_URL = "https://bmu.gnums.co.in/StudentPanel/STU_Student/STU_Student_ProfileView.aspx"

    async def fetch_student_profile(self, session_cookies: dict) -> ProfileData:
        try:
            cookies_jar = httpx.Cookies()
            for k, v in session_cookies.items():
                cookies_jar.set(k, v, domain="bmu.gnums.co.in")

            async with httpx.AsyncClient(
                cookies=cookies_jar,
                follow_redirects=True,
                timeout=config.REQUEST_TIMEOUT
            ) as client:
                resp = await client.get(self.PROFILE_URL)
                
                if resp.status_code != 200:
                    raise ExternalServiceError(f"Failed to fetch profile. Status: {resp.status_code}")

                soup = BeautifulSoup(resp.text, "html.parser")
                
                if soup.find("input", {"id": "txtUsername"}):
                     raise ProfileError("Invalid session or expired cookies.")

                data = self._parse_profile(soup)
                return ProfileData(**data)

        except ProfileError:
            raise
        except Exception as e:
            logger.error(f"Error fetching profile: {e}", exc_info=True)
            raise ExternalServiceError(f"Unexpected error: {e}")

    def _parse_profile(self, soup: BeautifulSoup) -> dict:
        def get_text(_id):
            el = soup.find(id=_id)
            return el.get_text(strip=True) if el else None

        personal_info = {
            "title": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblHonorific"),
            "student_name": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblStudentLCName"),
            "gender": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblGender"),
            "birth_date": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblBirthDate"),
            "birth_place": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblBirthPlace"),
            "religion": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblReligionID"),
            "caste_category": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblCasteCategoryID"),
            "caste": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblCasteID"),
            "domicile_state": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblStateType"),
            "nationality": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblNationalityCountryID"),
            "region": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblRegion"),
            "blood_group": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblBloodGroup"),
            "mother_tongue": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherTongueLanguageID"),
            "is_nri": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblIsNRI"),
            "is_economically_backward": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblIsEconomicallyBackward"),
            "aadhaar_card_no": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblAadhaarCardNo"),
            "aadhaar_name": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblNameAsPerAadhaarCard"),
            "appron_size": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblAppronSize"),
            "is_pwd": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblIsPWD"),
            "pwd_description": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPWDDescription") if get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblIsPWD") == "Yes" else None,
            "is_hostel": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblIsHostelFacilityRequired"),
            "hostel_description": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblHostelFacilityDescription") if get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblIsHostelFacilityRequired") == "Yes" else None,
            "family_annual_income": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblFamilyAnnualIncome"),
        }

        admission_info = {
            "program": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblProgramID"),
            "admission_quota": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblAdmissionQuotaID"),
            "admission_type": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblAdmissionTypeID"),
            "admission_semester": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblAdmissionSemester"),
            "admission_year": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblAdmissionYearID"),
            "admission_academic_year": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblAdmissionAcademicYearID"),
            "date_of_admission": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblAdmissionReportingDate"),
            "campus_reporting_date": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblCampusReportingDate"),
            "student_kit_issued": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblIsStudentKitIssued"),
            "student_kit_datetime": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblStudentKitIssuedDateTime"),
            "student_kit_issued_by": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblStudentKitIssuedByUserID"),
            "abc_no": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblABCID"),
            "allotted_category": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblAdmissionCasteCategoryID"),
        }

        contact_info = {
            "mobile": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPhoneStudent1"),
            "whatsapp": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblWhatsappNo"),
            "email": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblEmailAlternate") or get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblEmail"),
            "permanent_address": {
                "line1": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPermanentAddressLine1"),
                "line2": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPermanentAddressLine2"),
                "city": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPermanentCity"),
                "pincode": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPermanentPincode"),
                "taluka": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPermanentTaluka"),
                "district": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPermanentDistrictID"),
                "state": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPermanentStateID"),
                "country": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPermanentCountryID"),
            },
            "present_address": {
                "line1": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPresentAddressLine1"),
                "line2": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPresentAddressLine2"),
                "city": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPresentCity"),
                "pincode": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPresentPincode"),
                "taluka": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPresentTaluka"),
                "district": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPresentDistrictID"),
                "state": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPresentStateID"),
                "country": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblPresentCountryID"),
            },
        }

        parents_info = {
            "father": {
                "title": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblFatherHonorific"),
                "first_name": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblFatherName"),
                "mobile": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblFatherMobile"),
                "email": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblFatherEmail"),
                "qualification": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblFatherQualification"),
                "designation": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblFatherDesignation"),
                "occupation": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblFatherOccupation"),
                "organization": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblFatherOrganizationName"),
                "occupation_city": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblFatherOccupationCity"),
            },
            "mother": {
                "title": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherHonorific"),
                "first_name": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherName"),
                "mobile": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherMobile"),
                "email": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherEmail"),
                "qualification": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherQualification"),
                "designation": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherDesignation"),
                "occupation": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherOccupation"),
                "organization": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherOrganizationName"),
                "occupation_city": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherOccupationCity"),
            },
            "guardian": {
                "relation_type": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblGuardianRelationTypeID"),
                "first_name": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblGuardianName"),
                "mobile": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblGuardianMobile"),
                "email": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblGuardianEmail"),
                "qualification": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblGuardianQualification"),
                "occupation": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblGuardianOccupation"),
                "designation": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblGuardianDesignation"),
                "organization": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblGuardianOrganizationName"),
                "occupation_city": get_text("ctl00_cphPageContent_ucStudentInfoAdmission_lblGuardianOccupationCity"),
            }
        }

        education_qualification = {}
        edu_levels = ["SSC", "HSC", "Bachelor"]

        for idx, level in enumerate(edu_levels):
            prefix = f"ctl00_cphPageContent_ucStudentInfoAdmission_rpEducationQualification_ctl0{idx}_"
            edu_data = {
                "degree": clean_labelled_text(get_text(prefix + "divDegreeID")),
                "exam_name": clean_labelled_text(get_text(prefix + "divExamName")),
                "specialization": clean_labelled_text(get_text(prefix + "divSpecialization")),
                "result_class": clean_labelled_text(get_text(prefix + "divResultClass")),
                "board_university": clean_labelled_text(get_text(prefix + "divBoardUniversityID")),
                "school_college_name": clean_labelled_text(get_text(prefix + "divSchoolCollegeName")),
                "passing_month": clean_labelled_text(get_text(prefix + "divPassingMonth")),
                "seat_no": clean_labelled_text(get_text(prefix + "divSeatNo")),
                "total_mark": clean_labelled_text(get_text(prefix + "divTotalMark")),
                "obtained_mark": clean_labelled_text(get_text(prefix + "divObtainedMark")),
                "percentage": clean_labelled_text(get_text(prefix + "divPercentage")),
                "state_id": clean_labelled_text(get_text(prefix + "divStateID")),
                "passed_from_district": clean_labelled_text(get_text(prefix + "divDistrictID")),
                "place_of_study": clean_labelled_text(get_text(prefix + "divPlaceOfStudy")),
                "medium_of_instruction": clean_labelled_text(get_text(prefix + "divMediumofInstructionLanguageID")),
            }

            if level == "Bachelor":
                sgpa_el = soup.select_one("div.static-info:has(span:contains('SGPA')) div.gn-view-label-value span")
                cgpa_el = soup.select_one("div.static-info:has(span:contains('CGPA')) div.gn-view-label-value span")
                edu_data["sgpa"] = sgpa_el.get_text(strip=True) if sgpa_el else None
                edu_data["cgpa"] = cgpa_el.get_text(strip=True) if cgpa_el else None

            education_qualification[level] = edu_data

        return {
            "personal_info": personal_info,
            "admission_info": admission_info,
            "contact_info": contact_info,
            "parents_info": parents_info,
            "education_qualification": education_qualification
        }

student_profile_viewmodel = StudentProfileViewModel()
