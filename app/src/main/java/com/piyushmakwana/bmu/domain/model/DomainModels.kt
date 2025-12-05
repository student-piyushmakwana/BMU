package com.piyushmakwana.bmu.domain.model

data class PublicInfo(
    val latestNews: List<NewsItem>,
    val testimonials: List<TestimonialItem>,
    val banners: List<String>,
    val upcomingEvents: List<UpcomingEventItem>,
    val departments: List<Department> = emptyList()
)

data class NewsItem(
    val date: String,
    val description: String,
    val link: String
)

data class TestimonialItem(
    val name: String,
    val designation: String,
    val photoUrl: String,
    val message: String
)

data class UpcomingEventItem(
    val date: String,
    val description: String,
    val link: String
)

data class Department(
    val id: String,
    val bmuId: Int,
    val name: String,
    val shortName: String
)

data class DepartmentDetail(
    val id: String,
    val bmuId: Int,
    val name: String,
    val shortName: String,
    val director: Director,
    val faculty: List<Faculty>,
    val gallery: List<GalleryItem>,
    val infrastructure: List<InfrastructureItem>,
    val placement: List<PlacementMember>,
    val programs: Map<String, Program>,
    val studentsRecruited: List<StudentRecruited>
)

data class Director(
    val email: String,
    val message: String,
    val name: String,
    val photo: String,
    val qualification: String,
    val teachingExperience: String
)

data class Faculty(
    val designation: String,
    val email: String,
    val name: String,
    val photo: String,
    val qualification: String?,
    val specialization: String
)

data class GalleryItem(
    val images: List<String>,
    val title: String
)

data class InfrastructureItem(
    val images: List<String>,
    val title: String
)

data class PlacementMember(
    val designation: String,
    val email: String,
    val name: String,
    val phone: String,
    val photo: String,
    val qualification: String
)

data class Program(
    val description: List<String>,
    val semesters: List<Semester>
)

data class Semester(
    val semester: String,
    val subjects: List<Subject>
)

data class Subject(
    val subjectCode: String,
    val subjectName: String
)

data class StudentRecruited(
    val companyName: String,
    val departmentName: String,
    val srNo: String,
    val studentName: String
)