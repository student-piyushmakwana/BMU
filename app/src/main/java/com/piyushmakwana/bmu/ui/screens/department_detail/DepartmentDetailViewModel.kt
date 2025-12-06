package com.piyushmakwana.bmu.ui.screens.department_detail

import androidx.compose.runtime.State
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.piyushmakwana.bmu.common.Resource
import com.piyushmakwana.bmu.domain.model.DepartmentDetail
import com.piyushmakwana.bmu.domain.usecase.GetDepartmentDetailUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach

data class DepartmentDetailState(
    val isLoading: Boolean = false,
    val departmentDetail: DepartmentDetail? = null,
    val error: String = "",
    val shortName: String = ""
)

@HiltViewModel
class DepartmentDetailViewModel
@Inject
constructor(
    private val getDepartmentDetailUseCase: GetDepartmentDetailUseCase,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _state = mutableStateOf(DepartmentDetailState())
    val state: State<DepartmentDetailState> = _state

    init {
        val shortName = savedStateHandle.get<String>("shortName") ?: ""
        _state.value = _state.value.copy(shortName = shortName)

        savedStateHandle.get<String>("bmuId")?.toIntOrNull()?.let { bmuId ->
            getDepartmentDetail(bmuId)
        }
    }

    private fun getDepartmentDetail(bmuId: Int) {
        getDepartmentDetailUseCase(bmuId)
            .onEach { result ->
                when (result) {
                    is Resource.Success -> {
                        _state.value =
                            _state.value.copy(
                                departmentDetail = result.data,
                                isLoading = false,
                                error = ""
                            )
                    }
                    is Resource.Error -> {
                        _state.value =
                            _state.value.copy(
                                error = result.message
                                    ?: "An unexpected error occurred",
                                isLoading = false
                            )
                    }
                    is Resource.Loading -> {
                        _state.value = _state.value.copy(isLoading = true, error = "")
                    }
                }
            }
            .launchIn(viewModelScope)
    }
}