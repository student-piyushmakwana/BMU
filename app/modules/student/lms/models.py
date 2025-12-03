from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class LMSSubject(BaseModel):
    subject_name: Optional[str]
    semester: Optional[str]
    content_count: Optional[int]
    link: Optional[str]

class LMSDashboardData(BaseModel):
    subjects: List[LMSSubject]

class SubjectDetails(BaseModel):
    subject_name: Optional[str]
    semester: Optional[str]
    faculty: Optional[str]
    course: Optional[str]
    base_department: Optional[str]
    elective: Optional[str]
    common_subject: Optional[str]

class SyllabusInfo(BaseModel):
    postback_id: Optional[str]
    form_action: Optional[str]
    title: Optional[str]

class StaffDetails(BaseModel):
    name: Optional[str]
    designation: Optional[str]
    email: Optional[str]
    image_url: Optional[str]

class Unit(BaseModel):
    sr_no: Optional[str]
    unit_name: Optional[str]
    weightage: Optional[str]
    teaching_hours: Optional[str]

class ContentItem(BaseModel):
    sr_no: Optional[str]
    title: Optional[str]
    link: Optional[str]
    download_link: Optional[str]
    updated_date: Optional[str]
    updated_time: Optional[str]
    prepared_by: Optional[str]
    view_status: Optional[str]
    rating: Optional["ContentRating"]

class RatingOption(BaseModel):
    star_value: int
    postback_id: str

class ContentRating(BaseModel):
    current_rating: Optional[str]
    options: List[RatingOption]

class ContentCategory(BaseModel):
    category_name: Optional[str]
    count: Optional[int]
    items: List[ContentItem]

class ExamScheme(BaseModel):
    internal_theory_max: Optional[str]
    internal_theory_pass: Optional[str]
    internal_practical_max: Optional[str]
    internal_practical_pass: Optional[str]
    external_theory_max: Optional[str]
    external_theory_pass: Optional[str]
    external_practical_max: Optional[str]
    external_practical_pass: Optional[str]
    total_marks: Optional[str]
    exam_duration: Optional[str]

class TeachingScheme(BaseModel):
    practical_hours: Optional[str]
    lecture_hours: Optional[str]
    tutorial_hours: Optional[str]
    credits: Optional[str]

class LMSSubjectData(BaseModel):
    subject_details: SubjectDetails
    syllabus: Optional[SyllabusInfo]
    staff_details: Optional[StaffDetails]
    exam_scheme: Optional[ExamScheme]
    teaching_scheme: Optional[TeachingScheme]
    units: List[Unit]
    content_categories: List[ContentCategory]

class PDFResponse(BaseModel):
    pdf_base64: str
