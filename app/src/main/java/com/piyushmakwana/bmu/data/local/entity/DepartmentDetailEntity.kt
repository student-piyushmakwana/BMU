package com.piyushmakwana.bmu.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.piyushmakwana.bmu.data.remote.dto.DepartmentDetailDataDto

@Entity
data class DepartmentDetailEntity(@PrimaryKey val bmuId: Int, val data: DepartmentDetailDataDto)
