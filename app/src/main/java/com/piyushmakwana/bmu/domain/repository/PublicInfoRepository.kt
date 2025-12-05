package com.piyushmakwana.bmu.domain.repository

import com.piyushmakwana.bmu.data.remote.dto.DepartmentsResponseDto
import com.piyushmakwana.bmu.data.remote.dto.PublicInfoResponseDto

interface PublicInfoRepository {
    suspend fun getPublicInfo(): PublicInfoResponseDto
    suspend fun getDepartments(): DepartmentsResponseDto
}