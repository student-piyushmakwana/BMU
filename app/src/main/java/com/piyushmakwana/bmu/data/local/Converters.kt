package com.piyushmakwana.bmu.data.local

import androidx.room.TypeConverter
import com.piyushmakwana.bmu.data.remote.dto.DepartmentDetailDataDto
import com.piyushmakwana.bmu.data.remote.dto.DepartmentDto
import com.piyushmakwana.bmu.data.remote.dto.PublicInfoDataDto
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

class Converters {
    private val json = Json { ignoreUnknownKeys = true }

    @TypeConverter
    fun fromPublicInfoDataDto(data: PublicInfoDataDto): String {
        return json.encodeToString(data)
    }

    @TypeConverter
    fun toPublicInfoDataDto(jsonString: String): PublicInfoDataDto {
        return json.decodeFromString(jsonString)
    }

    @TypeConverter
    fun fromDepartmentDetailDataDto(data: DepartmentDetailDataDto): String {
        return json.encodeToString(data)
    }

    @TypeConverter
    fun toDepartmentDetailDataDto(jsonString: String): DepartmentDetailDataDto {
        return json.decodeFromString(jsonString)
    }

    @TypeConverter
    fun fromDepartmentDtoList(data: List<DepartmentDto>): String {
        return json.encodeToString(data)
    }

    @TypeConverter
    fun toDepartmentDtoList(jsonString: String): List<DepartmentDto> {
        return json.decodeFromString(jsonString)
    }
}
