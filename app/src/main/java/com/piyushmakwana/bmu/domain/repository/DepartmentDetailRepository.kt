package com.piyushmakwana.bmu.domain.repository

import com.piyushmakwana.bmu.data.remote.dto.DepartmentDetailResponseDto

interface DepartmentDetailRepository {
    suspend fun getDepartmentDetails(bmuId: Int): DepartmentDetailResponseDto
}