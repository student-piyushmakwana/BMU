package com.piyushmakwana.bmu.data.remote

import com.piyushmakwana.bmu.data.remote.dto.DepartmentsResponseDto
import com.piyushmakwana.bmu.data.remote.dto.PublicInfoResponseDto
import retrofit2.http.GET

interface BMUApi {
    @GET("v2/public/info")
    suspend fun getPublicInfo(): PublicInfoResponseDto

    @GET("v2/departments")
    suspend fun getDepartments(): DepartmentsResponseDto
}