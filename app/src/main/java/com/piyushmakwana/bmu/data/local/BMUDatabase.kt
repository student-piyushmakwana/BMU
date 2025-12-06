package com.piyushmakwana.bmu.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.piyushmakwana.bmu.data.local.entity.DepartmentDetailEntity
import com.piyushmakwana.bmu.data.local.entity.DepartmentsEntity
import com.piyushmakwana.bmu.data.local.entity.PublicInfoEntity

@Database(
        entities =
                [PublicInfoEntity::class, DepartmentsEntity::class, DepartmentDetailEntity::class],
        version = 1,
        exportSchema = false
)
@TypeConverters(Converters::class)
abstract class BMUDatabase : RoomDatabase() {
    abstract fun bmuDao(): BMUDao
}
