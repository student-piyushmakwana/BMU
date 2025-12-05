package com.piyushmakwana.bmu.data.remote

import com.piyushmakwana.bmu.data.remote.dto.DepartmentDetailRequestDto
import com.piyushmakwana.bmu.data.remote.dto.DepartmentDetailResponseDto
import com.piyushmakwana.bmu.data.remote.dto.DepartmentsResponseDto
import com.piyushmakwana.bmu.data.remote.dto.PublicInfoResponseDto
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface BMUApi {
    @GET("v2/public/info")
    suspend fun getPublicInfo(): PublicInfoResponseDto

    @GET("v2/departments")
    suspend fun getDepartments(): DepartmentsResponseDto

    @POST("v2/department/details")
    suspend fun getDepartmentDetails(
        @Body request: DepartmentDetailRequestDto
    ): DepartmentDetailResponseDto
}