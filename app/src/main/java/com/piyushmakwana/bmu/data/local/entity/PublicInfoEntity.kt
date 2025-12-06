package com.piyushmakwana.bmu.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.piyushmakwana.bmu.data.remote.dto.PublicInfoDataDto

@Entity data class PublicInfoEntity(@PrimaryKey val id: Int = 1, val data: PublicInfoDataDto)
