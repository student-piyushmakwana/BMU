from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class DepartmentListItem(BaseModel):
    bmu_id: int
    name: str
    short_name: str

class Director(BaseModel):
    photo: Optional[str]
    name: Optional[str]
    qualification: Optional[str]
    email: Optional[str]
    teaching_experience: Optional[str]
    message: Optional[str]

class FacultyMember(BaseModel):
    photo: Optional[str]
    name: Optional[str]
    designation: Optional[str]
    qualification: Optional[str]
    specialization: Optional[str]
    email: Optional[str]

class InfrastructureSection(BaseModel):
    title: Optional[str]
    images: List[str]

class GallerySection(BaseModel):
    title: Optional[str]
    images: List[str]

class PlacementMember(BaseModel):
    photo: Optional[str]
    name: Optional[str]
    qualification: Optional[str]
    designation: Optional[str]
    phone: Optional[str]
    email: Optional[str]

class StudentRecruited(BaseModel):
    sr_no: Optional[str]
    student_name: Optional[str]
    company_name: Optional[str]
    department_name: Optional[str]

class Subject(BaseModel):
    subject_code: Optional[str]
    subject_name: Optional[str]

class Semester(BaseModel):
    semester: Optional[str]
    subjects: List[Subject]

class ProgramDetails(BaseModel):
    description: List[str]
    semesters: List[Semester]

class InstituteDetails(BaseModel):
    director: Optional[Director]
    faculty: List[FacultyMember]
    infrastructure: List[InfrastructureSection]
    gallery: List[GallerySection]
    placement: List[PlacementMember]
    students_recruited: List[StudentRecruited]
    programs: Dict[str, ProgramDetails]
