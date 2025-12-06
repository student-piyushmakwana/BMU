package com.piyushmakwana.bmu.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.piyushmakwana.bmu.data.remote.dto.DepartmentDto

@Entity data class DepartmentsEntity(@PrimaryKey val id: Int = 1, val data: List<DepartmentDto>)
