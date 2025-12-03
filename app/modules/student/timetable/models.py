from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Lecture(BaseModel):
    batch: Optional[str]
    subject: Optional[str]
    faculty: Optional[str]
    room: Optional[str]

class DaySchedule(BaseModel):
    day: str
    lectures: List[Lecture]

class TimeSlot(BaseModel):
    time_slot: str
    schedule: List[DaySchedule]

class TimetableData(BaseModel):
    institute: Optional[str]
    class_info: Optional[str]
    effective_from: Optional[str]
    timetable: List[TimeSlot]
