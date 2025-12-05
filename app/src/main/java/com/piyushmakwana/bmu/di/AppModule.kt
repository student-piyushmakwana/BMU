package com.piyushmakwana.bmu.di

import com.piyushmakwana.bmu.common.Constants
import com.piyushmakwana.bmu.data.remote.BMUApi
import com.piyushmakwana.bmu.data.repository.PublicInfoRepositoryImpl
import com.piyushmakwana.bmu.domain.repository.PublicInfoRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        val logging = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
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
    fun providePublicInfoRepository(api: BMUApi): PublicInfoRepository {
        return PublicInfoRepositoryImpl(api)
    }
}