package com.piyushmakwana.bmu.data.remote.dto

import com.piyushmakwana.bmu.domain.model.DepartmentDetail
import com.piyushmakwana.bmu.domain.model.Director
import com.piyushmakwana.bmu.domain.model.Faculty
import com.piyushmakwana.bmu.domain.model.GalleryItem
import com.piyushmakwana.bmu.domain.model.InfrastructureItem
import com.piyushmakwana.bmu.domain.model.PlacementMember
import com.piyushmakwana.bmu.domain.model.Program
import com.piyushmakwana.bmu.domain.model.Semester
import com.piyushmakwana.bmu.domain.model.StudentRecruited
import com.piyushmakwana.bmu.domain.model.Subject
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class DepartmentDetailResponseDto(
    @SerialName("data")
    val data: DepartmentDetailDataDto,

    @SerialName("message")
    val message: String,

    @SerialName("success")
    val success: Boolean
)

@Serializable
data class DepartmentDetailDataDto(
    @SerialName("_id")
    val id: String,

    @SerialName("bmu_id")
    val bmuId: Int,

    @SerialName("name")
    val name: String,

    @SerialName("short_name")
    val shortName: String,

    @SerialName("director")
    val director: DirectorDto,

    @SerialName("faculty")
    val faculty: List<FacultyDto>,

    @SerialName("gallery")
    val gallery: List<GalleryItemDto>,

    @SerialName("infrastructure")
    val infrastructure: List<InfrastructureItemDto>,

    @SerialName("placement")
    val placement: List<PlacementMemberDto>,

    @SerialName("programs")
    val programs: Map<String, ProgramDto>,

    @SerialName("students_recruited")
    val studentsRecruited: List<StudentRecruitedDto>
)

@Serializable
data class DirectorDto(
    @SerialName("email")
    val email: String,

    @SerialName("message")
    val message: String,

    @SerialName("name")
    val name: String,

    @SerialName("photo")
    val photo: String,

    @SerialName("qualification")
    val qualification: String,

    @SerialName("teaching_experience")
    val teachingExperience: String
)

@Serializable
data class FacultyDto(
    @SerialName("designation")
    val designation: String,

    @SerialName("email")
    val email: String,

    @SerialName("name")
    val name: String,

    @SerialName("photo")
    val photo: String,

    @SerialName("qualification")
    val qualification: String? = null,

    @SerialName("specialization")
    val specialization: String
)

@Serializable
data class GalleryItemDto(
    @SerialName("images")
    val images: List<String>,

    @SerialName("title")
    val title: String
)

@Serializable
data class InfrastructureItemDto(
    @SerialName("images")
    val images: List<String>,

    @SerialName("title")
    val title: String
)

@Serializable
data class PlacementMemberDto(
    @SerialName("designation")
    val designation: String,

    @SerialName("email")
    val email: String,

    @SerialName("name")
    val name: String,

    @SerialName("phone")
    val phone: String,

    @SerialName("photo")
    val photo: String,

    @SerialName("qualification")
    val qualification: String
)

@Serializable
data class ProgramDto(
    @SerialName("description")
    val description: List<String>,

    @SerialName("semesters")
    val semesters: List<SemesterDto>
)

@Serializable
data class SemesterDto(
    @SerialName("semester")
    val semester: String,

    @SerialName("subjects")
    val subjects: List<SubjectDto>
)

@Serializable
data class SubjectDto(
    @SerialName("subject_code")
    val subjectCode: String,

    @SerialName("subject_name")
    val subjectName: String
)

@Serializable
data class StudentRecruitedDto(
    @SerialName("company_name")
    val companyName: String,

    @SerialName("department_name")
    val departmentName: String,

    @SerialName("sr_no")
    val srNo: String,

    @SerialName("student_name")
    val studentName: String
)

fun DepartmentDetailDataDto.toDomain(): DepartmentDetail {
    return DepartmentDetail(
        id = id,
        bmuId = bmuId,
        name = name,
        shortName = shortName,
        director = director.toDomain(),
        faculty = faculty.map { it.toDomain() },
        gallery = gallery.map { it.toDomain() },
        infrastructure = infrastructure.map { it.toDomain() },
        placement = placement.map { it.toDomain() },
        programs = programs.map { (key, value) -> key to value.toDomain() }.toMap(),
        studentsRecruited = studentsRecruited.map { it.toDomain() }
    )
}

fun DirectorDto.toDomain() = Director(
    email = email,
    message = message,
    name = name,
    photo = photo,
    qualification = qualification,
    teachingExperience = teachingExperience
)

fun FacultyDto.toDomain() = Faculty(
    designation = designation,
    email = email,
    name = name,
    photo = photo,
    qualification = qualification,
    specialization = specialization
)

fun GalleryItemDto.toDomain() = GalleryItem(
    images = images,
    title = title
)

fun InfrastructureItemDto.toDomain() = InfrastructureItem(
    images = images,
    title = title
)

fun PlacementMemberDto.toDomain() = PlacementMember(
    designation = designation,
    email = email,
    name = name,
    phone = phone,
    photo = photo,
    qualification = qualification
)

fun ProgramDto.toDomain() = Program(
    description = description,
    semesters = semesters.map { it.toDomain() }
)

fun SemesterDto.toDomain() = Semester(
    semester = semester,
    subjects = subjects.map { it.toDomain() }
)

fun SubjectDto.toDomain() = Subject(
    subjectCode = subjectCode,
    subjectName = subjectName
)

fun StudentRecruitedDto.toDomain() = StudentRecruited(
    companyName = companyName,
    departmentName = departmentName,
    srNo = srNo,
    studentName = studentName
)