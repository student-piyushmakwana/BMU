package com.piyushmakwana.bmu.ui.screens.public_info

import androidx.compose.runtime.State
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.piyushmakwana.bmu.common.Resource
import com.piyushmakwana.bmu.domain.model.PublicInfo
import com.piyushmakwana.bmu.domain.usecase.GetPublicInfoUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import javax.inject.Inject

data class PublicInfoState(
    val isLoading: Boolean = false,
    val publicInfo: PublicInfo? = null,
    val error: String = ""
)

@HiltViewModel
class PublicInfoViewModel @Inject constructor(
    private val getPublicInfoUseCase: GetPublicInfoUseCase
) : ViewModel() {

    private val _state = mutableStateOf(PublicInfoState())
    val state: State<PublicInfoState> = _state

    init {
        getPublicInfo()
    }

    private fun getPublicInfo() {
        getPublicInfoUseCase().onEach { result ->
            when (result) {
                is Resource.Success -> {
                    _state.value = PublicInfoState(publicInfo = result.data)
                }
                is Resource.Error -> {
                    _state.value = PublicInfoState(
                        error = result.message ?: "An unexpected error occurred"
                    )
                }
                is Resource.Loading -> {
                    _state.value = PublicInfoState(isLoading = true)
                }
            }
        }.launchIn(viewModelScope)
    }
}