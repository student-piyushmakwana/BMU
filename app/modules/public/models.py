from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Event(BaseModel):
    date: Optional[str]
    description: Optional[str]
    link: Optional[str]

class NewsItem(BaseModel):
    date: Optional[str]
    description: Optional[str]
    link: Optional[str]

class Testimonial(BaseModel):
    name: Optional[str]
    designation: Optional[str]
    testimonial: Optional[str]
    photo: Optional[str]

class PublicInfoData(BaseModel):
    upcoming_events: List[Event]
    latest_news: List[NewsItem]
    student_testimonials: List[Testimonial]
    university_banner: List[str]
