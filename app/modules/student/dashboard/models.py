from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class PersonalInfo(BaseModel):
    full_name: Optional[str]
    profile_image_main: Optional[str]
    profile_image_responsive: Optional[str]
    birth_date: Optional[str]
    gender: Optional[str]

class EducationInfo(BaseModel):
    course_name: Optional[str]
    semester: Optional[str]
    enrollment_no: Optional[str]
    abc_id: Optional[str]
    status: Optional[str]
    division: Optional[str]
    batch_no: Optional[str]
    roll_no: Optional[str]

class ContactInfo(BaseModel):
    mobile_no: Optional[str]
    email: Optional[str]

class FamilyInfo(BaseModel):
    father_name: Optional[str]
    father_mobile: Optional[str]
    mother_name: Optional[str]
    mother_mobile: Optional[str]

class Assignment(BaseModel):
    sr_no: Optional[str]
    subject: Optional[str]
    assignment_name: Optional[str]
    last_date: Optional[str]

class DashboardData(BaseModel):
    personal: PersonalInfo
    education: EducationInfo
    contact: ContactInfo
    family: FamilyInfo
    pending_assignments: List[Assignment]
