package com.piyushmakwana.bmu.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.piyushmakwana.bmu.data.local.entity.DepartmentDetailEntity
import com.piyushmakwana.bmu.data.local.entity.DepartmentsEntity
import com.piyushmakwana.bmu.data.local.entity.PublicInfoEntity

@Dao
interface BMUDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPublicInfo(entity: PublicInfoEntity)

    @Query("SELECT * FROM PublicInfoEntity WHERE id = 1")
    suspend fun getPublicInfo(): PublicInfoEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertDepartments(entity: DepartmentsEntity)

    @Query("SELECT * FROM DepartmentsEntity WHERE id = 1")
    suspend fun getDepartments(): DepartmentsEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertDepartmentDetail(entity: DepartmentDetailEntity)

    @Query("SELECT * FROM DepartmentDetailEntity WHERE bmuId = :bmuId")
    suspend fun getDepartmentDetail(bmuId: Int): DepartmentDetailEntity?
}
