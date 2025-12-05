package com.piyushmakwana.bmu.data.remote.dto

import com.piyushmakwana.bmu.domain.model.NewsItem
import com.piyushmakwana.bmu.domain.model.PublicInfo
import com.piyushmakwana.bmu.domain.model.TestimonialItem
import com.piyushmakwana.bmu.domain.model.UpcomingEventItem
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class PublicInfoResponseDto(
    @SerialName("data")
    val data: PublicInfoDataDto,

    @SerialName("message")
    val message: String,

    @SerialName("success")
    val success: Boolean
)

@Serializable
data class PublicInfoDataDto(
    @SerialName("latest_news")
    val latestNews: List<NewsItemDto>,

    @SerialName("student_testimonials")
    val studentTestimonials: List<TestimonialDto>,

    @SerialName("university_banner")
    val universityBanner: List<String>,

    @SerialName("upcoming_events")
    val upcomingEvents: List<UpcomingEventDto>
)

@Serializable
data class NewsItemDto(
    @SerialName("date")
    val date: String,

    @SerialName("description")
    val description: String,

    @SerialName("link")
    val link: String
)

@Serializable
data class TestimonialDto(
    @SerialName("designation")
    val designation: String,

    @SerialName("name")
    val name: String,

    @SerialName("photo")
    val photo: String,

    @SerialName("testimonial")
    val testimonial: String
)

@Serializable
data class UpcomingEventDto(
    @SerialName("date")
    val date: String,

    @SerialName("description")
    val description: String,

    @SerialName("link")
    val link: String
)

fun PublicInfoDataDto.toDomain(): PublicInfo {
    return PublicInfo(
        latestNews = latestNews.map { it.toDomain() },
        testimonials = studentTestimonials.map { it.toDomain() },
        banners = universityBanner,
        upcomingEvents = upcomingEvents.map { it.toDomain() }
    )
}

fun NewsItemDto.toDomain() = NewsItem(date, description, link)
fun TestimonialDto.toDomain() = TestimonialItem(name, designation, photo, testimonial)
fun UpcomingEventDto.toDomain() = UpcomingEventItem(date, description, link)