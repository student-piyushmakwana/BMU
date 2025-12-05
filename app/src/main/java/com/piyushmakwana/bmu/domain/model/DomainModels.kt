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