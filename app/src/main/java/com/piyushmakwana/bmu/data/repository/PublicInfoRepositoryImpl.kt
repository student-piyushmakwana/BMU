package com.piyushmakwana.bmu.data.repository

import com.piyushmakwana.bmu.data.remote.BMUApi
import com.piyushmakwana.bmu.data.remote.dto.DepartmentsResponseDto
import com.piyushmakwana.bmu.data.remote.dto.PublicInfoResponseDto
import com.piyushmakwana.bmu.domain.repository.PublicInfoRepository
import javax.inject.Inject

class PublicInfoRepositoryImpl @Inject constructor(private val api: BMUApi) : PublicInfoRepository {

    override suspend fun getPublicInfo(): PublicInfoResponseDto {
        return api.getPublicInfo()
    }

    override suspend fun getDepartments(): DepartmentsResponseDto {
        return api.getDepartments()
    }
}