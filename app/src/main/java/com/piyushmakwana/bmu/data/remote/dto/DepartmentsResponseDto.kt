package com.piyushmakwana.bmu.data.remote.dto

import com.piyushmakwana.bmu.domain.model.Department
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class DepartmentsResponseDto(
    @SerialName("data")
    val data: List<DepartmentDto>,

    @SerialName("message")
    val message: String,

    @SerialName("success")
    val success: Boolean
)

@Serializable
data class DepartmentDto(
    @SerialName("_id")
    val id: String,

    @SerialName("bmu_id")
    val bmuId: Int,

    @SerialName("name")
    val name: String,

    @SerialName("short_name")
    val shortName: String
)

fun DepartmentDto.toDomain(): Department {
    return Department(
        id = id,
        bmuId = bmuId,
        name = name,
        shortName = shortName
    )
}
