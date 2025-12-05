package com.piyushmakwana.bmu.domain.usecase

import com.piyushmakwana.bmu.common.Resource
import com.piyushmakwana.bmu.data.remote.dto.toDomain
import com.piyushmakwana.bmu.domain.model.DepartmentDetail
import com.piyushmakwana.bmu.domain.repository.DepartmentDetailRepository
import java.io.IOException
import javax.inject.Inject
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import retrofit2.HttpException

class GetDepartmentDetailUseCase
@Inject
constructor(private val repository: DepartmentDetailRepository) {
    operator fun invoke(bmuId: Int): Flow<Resource<DepartmentDetail>> = flow {
        try {
            emit(Resource.Loading())
            val response = repository.getDepartmentDetails(bmuId)
            emit(Resource.Success(response.data.toDomain()))
        } catch (e: HttpException) {
            emit(Resource.Error(e.localizedMessage ?: "An unexpected error occurred"))
        } catch (e: IOException) {
            emit(Resource.Error("Couldn't reach server. Check your internet connection."))
        }
    }
}