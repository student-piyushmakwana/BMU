package com.piyushmakwana.bmu.domain.usecase

import com.piyushmakwana.bmu.common.Resource
import com.piyushmakwana.bmu.data.remote.dto.toDomain
import com.piyushmakwana.bmu.domain.model.PublicInfo
import com.piyushmakwana.bmu.domain.repository.PublicInfoRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import retrofit2.HttpException
import java.io.IOException
import javax.inject.Inject

class GetPublicInfoUseCase @Inject constructor(private val repository: PublicInfoRepository) {
    operator fun invoke(): Flow<Resource<PublicInfo>> = flow {
        try {
            emit(Resource.Loading())
            val publicInfoDef = repository.getPublicInfo()
            val departmentsDef = repository.getDepartments()

            val domainData =
                    publicInfoDef
                            .data
                            .toDomain()
                            .copy(departments = departmentsDef.data.map { it.toDomain() })
            emit(Resource.Success(domainData))
        } catch (e: HttpException) {
            emit(Resource.Error(e.localizedMessage ?: "An unexpected error occurred"))
        } catch (e: IOException) {
            emit(Resource.Error("Couldn't reach server. Check your internet connection."))
        }
    }
}