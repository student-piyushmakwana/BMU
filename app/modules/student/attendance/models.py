from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class TotalAttendance(BaseModel):
    total_day: Optional[str]
    present_day: Optional[str]
    absent_days: Optional[str]
    present_percentage: Optional[str]

class SemesterAttendance(BaseModel):
    current_semester: Optional[str]
    second_semester: Optional[str]
    first_semester: Optional[str]

class SubjectAttendance(BaseModel):
    sr_no: Optional[str]
    slot_type: Optional[str]
    course: Optional[str]
    conducted: Optional[str]
    present: Optional[str]
    absent: Optional[str]
    attendance_percentage: Optional[str]

class AttendanceSummary(BaseModel):
    semester_wise: SemesterAttendance
    total: TotalAttendance
    subjects: List[SubjectAttendance]

class AbsentSummary(BaseModel):
    partial_absent_days: Optional[str]
    full_absent_days: Optional[str]
    total_absent_slots: Optional[str]

class AbsentDay(BaseModel):
    sr_no: Optional[str]
    attendance_date: Optional[str]
    conducted: Optional[str]
    present: Optional[str]
    absent: Optional[str]
    view_link: Optional[str]

class AbsentTotal(BaseModel):
    total_conducted: Optional[str]
    total_present: Optional[str]
    total_absent: Optional[str]

class AbsentDaysData(BaseModel):
    summary: AbsentSummary
    absent_days: List[AbsentDay]
    total: AbsentTotal

class AttendanceRecord(BaseModel):
    sr_no: Optional[str]
    time: Optional[str]
    course: Optional[str]
    staff: Optional[str]
    slot_type: Optional[str]
    status: Optional[str]

class DateAttendanceTotal(BaseModel):
    conducted: str
    present: str
    absent: str

class DateAttendanceData(BaseModel):
    date: str
    records: List[AttendanceRecord]
    total: DateAttendanceTotal
