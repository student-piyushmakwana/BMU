package com.piyushmakwana.bmu.di

import android.content.Context
import androidx.room.Room
import com.piyushmakwana.bmu.common.Constants
import com.piyushmakwana.bmu.data.local.BMUDao
import com.piyushmakwana.bmu.data.local.BMUDatabase
import com.piyushmakwana.bmu.data.remote.BMUApi
import com.piyushmakwana.bmu.data.repository.DepartmentDetailRepositoryImpl
import com.piyushmakwana.bmu.data.repository.PublicInfoRepositoryImpl
import com.piyushmakwana.bmu.domain.repository.DepartmentDetailRepository
import com.piyushmakwana.bmu.domain.repository.PublicInfoRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import java.util.concurrent.TimeUnit
import javax.inject.Singleton
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideBMUDatabase(@ApplicationContext context: Context): BMUDatabase {
        return Room.databaseBuilder(context, BMUDatabase::class.java, "bmu_db").build()
    }

    @Provides
    @Singleton
    fun provideBMUDao(database: BMUDatabase): BMUDao {
        return database.bmuDao()
    }

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        val logging = HttpLoggingInterceptor().apply { level = HttpLoggingInterceptor.Level.BODY }
        return OkHttpClient.Builder()
                .addInterceptor(logging)
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .build()
    }

    @Provides
    @Singleton
    fun provideBMUApi(okHttpClient: OkHttpClient): BMUApi {
        val json = Json {
            ignoreUnknownKeys = true
            isLenient = true
        }
        val contentType = "application/json".toMediaType()

        return Retrofit.Builder()
                .baseUrl(Constants.BASE_URL)
                .client(okHttpClient)
                .addConverterFactory(json.asConverterFactory(contentType))
                .build()
                .create(BMUApi::class.java)
    }

    @Provides
    @Singleton
    fun providePublicInfoRepository(api: BMUApi, dao: BMUDao): PublicInfoRepository {
        return PublicInfoRepositoryImpl(api, dao)
    }

    @Provides
    @Singleton
    fun provideDepartmentDetailRepository(api: BMUApi, dao: BMUDao): DepartmentDetailRepository {
        return DepartmentDetailRepositoryImpl(api, dao)
    }
}
