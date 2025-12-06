package com.piyushmakwana.bmu.data.repository

import com.piyushmakwana.bmu.data.local.BMUDao
import com.piyushmakwana.bmu.data.local.entity.DepartmentDetailEntity
import com.piyushmakwana.bmu.data.remote.BMUApi
import com.piyushmakwana.bmu.data.remote.dto.DepartmentDetailRequestDto
import com.piyushmakwana.bmu.data.remote.dto.DepartmentDetailResponseDto
import com.piyushmakwana.bmu.domain.repository.DepartmentDetailRepository
import javax.inject.Inject
import kotlinx.coroutines.delay

class DepartmentDetailRepositoryImpl
@Inject
constructor(private val api: BMUApi, private val dao: BMUDao) : DepartmentDetailRepository {

    override suspend fun getDepartmentDetails(bmuId: Int): DepartmentDetailResponseDto {
        return try {
            val response = api.getDepartmentDetails(DepartmentDetailRequestDto(bmuId))
            dao.insertDepartmentDetail(DepartmentDetailEntity(bmuId = bmuId, data = response.data))
            response
        } catch (e: Exception) {
            val cached = dao.getDepartmentDetail(bmuId)
            if (cached != null) {
                delay(1000)
                DepartmentDetailResponseDto(
                    data = cached.data,
                    message = "Loaded from cache",
                    success = true
                )
            } else {
                throw e
            }
        }
    }
}