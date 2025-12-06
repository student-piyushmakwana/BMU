package com.piyushmakwana.bmu.data.repository

import com.piyushmakwana.bmu.data.local.BMUDao
import com.piyushmakwana.bmu.data.local.entity.DepartmentsEntity
import com.piyushmakwana.bmu.data.local.entity.PublicInfoEntity
import com.piyushmakwana.bmu.data.remote.BMUApi
import com.piyushmakwana.bmu.data.remote.dto.DepartmentsResponseDto
import com.piyushmakwana.bmu.data.remote.dto.PublicInfoResponseDto
import com.piyushmakwana.bmu.domain.repository.PublicInfoRepository
import javax.inject.Inject
import kotlinx.coroutines.delay

class PublicInfoRepositoryImpl
@Inject
constructor(private val api: BMUApi, private val dao: BMUDao) : PublicInfoRepository {

    override suspend fun getPublicInfo(): PublicInfoResponseDto {
        return try {
            val response = api.getPublicInfo()
            dao.insertPublicInfo(PublicInfoEntity(data = response.data))
            response
        } catch (e: Exception) {
            val cached = dao.getPublicInfo()
            if (cached != null) {
                delay(1000)
                PublicInfoResponseDto(
                    data = cached.data,
                    message = "Loaded from cache",
                    success = true
                )
            } else {
                throw e
            }
        }
    }

    override suspend fun getDepartments(): DepartmentsResponseDto {
        return try {
            val response = api.getDepartments()
            dao.insertDepartments(DepartmentsEntity(data = response.data))
            response
        } catch (e: Exception) {
            val cached = dao.getDepartments()
            if (cached != null) {
                delay(1000)
                DepartmentsResponseDto(
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