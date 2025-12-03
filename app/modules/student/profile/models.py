from pydantic import BaseModel
from typing import Optional, Dict, Any

class PersonalInfo(BaseModel):
    title: Optional[str]
    student_name: Optional[str]
    gender: Optional[str]
    birth_date: Optional[str]
    birth_place: Optional[str]
    religion: Optional[str]
    caste_category: Optional[str]
    caste: Optional[str]
    domicile_state: Optional[str]
    nationality: Optional[str]
    region: Optional[str]
    blood_group: Optional[str]
    mother_tongue: Optional[str]
    is_nri: Optional[str]
    is_economically_backward: Optional[str]
    aadhaar_card_no: Optional[str]
    aadhaar_name: Optional[str]
    appron_size: Optional[str]
    is_pwd: Optional[str]
    pwd_description: Optional[str]
    is_hostel: Optional[str]
    hostel_description: Optional[str]
    family_annual_income: Optional[str]

class AdmissionInfo(BaseModel):
    program: Optional[str]
    admission_quota: Optional[str]
    admission_type: Optional[str]
    admission_semester: Optional[str]
    admission_year: Optional[str]
    admission_academic_year: Optional[str]
    date_of_admission: Optional[str]
    campus_reporting_date: Optional[str]
    student_kit_issued: Optional[str]
    student_kit_datetime: Optional[str]
    student_kit_issued_by: Optional[str]
    abc_no: Optional[str]
    allotted_category: Optional[str]

class Address(BaseModel):
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    pincode: Optional[str]
    taluka: Optional[str]
    district: Optional[str]
    state: Optional[str]
    country: Optional[str]

class ContactInfo(BaseModel):
    mobile: Optional[str]
    whatsapp: Optional[str]
    email: Optional[str]
    permanent_address: Address
    present_address: Address

class ParentDetails(BaseModel):
    title: Optional[str] = None
    first_name: Optional[str]
    mobile: Optional[str]
    email: Optional[str]
    qualification: Optional[str]
    designation: Optional[str] = None
    occupation: Optional[str]
    organization: Optional[str] = None
    occupation_city: Optional[str] = None
    relation_type: Optional[str] = None

class ParentsInfo(BaseModel):
    father: ParentDetails
    mother: ParentDetails
    guardian: ParentDetails

class EducationDetail(BaseModel):
    degree: Optional[str]
    exam_name: Optional[str]
    specialization: Optional[str]
    result_class: Optional[str]
    board_university: Optional[str]
    school_college_name: Optional[str]
    passing_month: Optional[str]
    seat_no: Optional[str]
    total_mark: Optional[str]
    obtained_mark: Optional[str]
    percentage: Optional[str]
    state_id: Optional[str]
    passed_from_district: Optional[str]
    place_of_study: Optional[str]
    medium_of_instruction: Optional[str]
    sgpa: Optional[str] = None
    cgpa: Optional[str] = None

class ProfileData(BaseModel):
    personal_info: PersonalInfo
    admission_info: AdmissionInfo
    contact_info: ContactInfo
    parents_info: ParentsInfo
    education_qualification: Dict[str, EducationDetail]
