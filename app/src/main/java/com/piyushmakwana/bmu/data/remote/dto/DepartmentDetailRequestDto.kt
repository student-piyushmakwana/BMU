package com.piyushmakwana.bmu.data.remote.dto

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class DepartmentDetailRequestDto(
    @SerialName("bmu_id")
    val bmuId: Int
)