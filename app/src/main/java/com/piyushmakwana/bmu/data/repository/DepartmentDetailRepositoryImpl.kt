package com.piyushmakwana.bmu.data.repository

import com.piyushmakwana.bmu.data.remote.BMUApi
import com.piyushmakwana.bmu.data.remote.dto.DepartmentDetailRequestDto
import com.piyushmakwana.bmu.data.remote.dto.DepartmentDetailResponseDto
import com.piyushmakwana.bmu.domain.repository.DepartmentDetailRepository
import javax.inject.Inject

class DepartmentDetailRepositoryImpl @Inject constructor(private val api: BMUApi) :
    DepartmentDetailRepository {

    override suspend fun getDepartmentDetails(bmuId: Int): DepartmentDetailResponseDto {
        return api.getDepartmentDetails(DepartmentDetailRequestDto(bmuId))
    }
}
