package com.piyushmakwana.bmu.ui.screens.department_detail

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.blur
import androidx.compose.ui.unit.dp
import androidx.hilt.lifecycle.viewmodel.compose.hiltViewModel
import androidx.navigation.NavController
import com.piyushmakwana.bmu.domain.model.GalleryItem
import com.piyushmakwana.bmu.domain.model.InfrastructureItem
import com.piyushmakwana.bmu.ui.screens.department_detail.components.DepartmentDetailBottomSheet
import com.piyushmakwana.bmu.ui.screens.department_detail.components.DepartmentDetailShimmer
import com.piyushmakwana.bmu.ui.screens.department_detail.components.DepartmentInfoCard
import com.piyushmakwana.bmu.ui.screens.department_detail.components.DepartmentStatisticsSection
import com.piyushmakwana.bmu.ui.screens.department_detail.components.DirectorCard
import com.piyushmakwana.bmu.ui.screens.department_detail.components.EmptyStateSection
import com.piyushmakwana.bmu.ui.screens.department_detail.components.FacultyCard
import com.piyushmakwana.bmu.ui.screens.department_detail.components.FullScreenProfileImage
import com.piyushmakwana.bmu.ui.screens.department_detail.components.GallerySection
import com.piyushmakwana.bmu.ui.screens.department_detail.components.InfrastructureSection
import com.piyushmakwana.bmu.ui.screens.department_detail.components.PlacementMemberCard
import com.piyushmakwana.bmu.ui.screens.department_detail.components.ProgramSection
import com.piyushmakwana.bmu.ui.screens.public_info.components.ErrorState
import com.piyushmakwana.bmu.ui.screens.public_info.components.NativeBackTopBar
import com.piyushmakwana.bmu.ui.screens.public_info.components.NativeSectionHeader

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DepartmentDetailScreen(
    navController: NavController,
    viewModel: DepartmentDetailViewModel = hiltViewModel()
) {
    val state = viewModel.state.value

    var selectedInfrastructure by remember { mutableStateOf<InfrastructureItem?>(null) }
    var selectedGallery by remember { mutableStateOf<GalleryItem?>(null) }
    var selectedStudentGroup by remember { mutableStateOf<String?>(null) }
    var selectedProfileImage by remember { mutableStateOf<String?>(null) }
    var selectedFaculty by remember {
        mutableStateOf<com.piyushmakwana.bmu.domain.model.Faculty?>(null)
    }
    var selectedPlacementMember by remember {
        mutableStateOf<com.piyushmakwana.bmu.domain.model.PlacementMember?>(null)
    }
    var showBottomSheet by remember { mutableStateOf(false) }
    var isProgramsExpanded by remember { mutableStateOf(false) }

    if (selectedInfrastructure != null ||
        selectedGallery != null ||
        selectedStudentGroup != null ||
        selectedFaculty != null ||
        selectedPlacementMember != null
    ) {
        showBottomSheet = true
    }

    val blurModifier = if (selectedProfileImage != null) Modifier.blur(16.dp) else Modifier

    Box(modifier = Modifier.fillMaxSize()) {
        Scaffold(
            topBar = {
                NativeBackTopBar(
                    title =
                        state.shortName.ifEmpty {
                            state.departmentDetail?.shortName ?: "Department Details"
                        },
                    onBackClick = { navController.popBackStack() },
                    maxLines = 2
                )
            },
            containerColor = MaterialTheme.colorScheme.surface,
            modifier = Modifier.fillMaxSize().then(blurModifier)
        ) { paddingValues ->
            Box(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
                if (state.departmentDetail != null) {
                    val detail = state.departmentDetail
                    val programsList =
                        remember(detail.programs) { detail.programs.entries.toList() }

                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(bottom = 48.dp)
                    ) {
                        item { Spacer(modifier = Modifier.height(16.dp)) }

                        item {
                            DepartmentInfoCard(
                                departmentName = detail.name,
                                modifier = Modifier.padding(horizontal = 24.dp)
                            )
                            Spacer(modifier = Modifier.height(32.dp))
                        }

                        val isDetailEmpty =
                            detail.director == null &&
                                    detail.faculty.isEmpty() &&
                                    detail.gallery.isEmpty() &&
                                    detail.infrastructure.isEmpty() &&
                                    detail.placement.isEmpty() &&
                                    detail.programs.isEmpty() &&
                                    detail.studentsRecruited.isEmpty()

                        if (isDetailEmpty) {
                            item {
                                EmptyStateSection(
                                    modifier = Modifier.fillParentMaxHeight(0.7f)
                                )
                            }
                        } else {
                            if (detail.director != null && !detail.director.name.isNullOrBlank()) {
                                item {
                                    NativeSectionHeader(title = "Director")
                                    Spacer(modifier = Modifier.height(16.dp))
                                    DirectorCard(
                                        director = detail.director,
                                        modifier = Modifier.padding(horizontal = 24.dp),
                                        onImageLongClick = { selectedProfileImage = it }
                                    )
                                    Spacer(modifier = Modifier.height(32.dp))
                                }
                            }

                            if (detail.faculty.isNotEmpty()) {
                                item {
                                    NativeSectionHeader(title = "Faculty Members")
                                    Spacer(modifier = Modifier.height(16.dp))
                                    LazyRow(
                                        contentPadding = PaddingValues(horizontal = 24.dp),
                                        horizontalArrangement = Arrangement.spacedBy(16.dp)
                                    ) {
                                        items(items = detail.faculty) { faculty ->
                                            FacultyCard(
                                                faculty = faculty,
                                                onImageLongClick = {
                                                    selectedProfileImage = it
                                                },
                                                onClick = { selectedFaculty = faculty }
                                            )
                                        }
                                    }
                                    Spacer(modifier = Modifier.height(32.dp))
                                }
                            }

                            if (detail.programs.isNotEmpty()) {
                                item {
                                    NativeSectionHeader(title = "Programs Offered")
                                    Spacer(modifier = Modifier.height(16.dp))
                                }

                                val visiblePrograms =
                                    if (isProgramsExpanded) programsList
                                    else programsList.take(4)

                                items(items = visiblePrograms, key = { it.key }) { (name, program)
                                    ->
                                    ProgramSection(
                                        programName = name,
                                        program = program,
                                        modifier =
                                            Modifier.padding(
                                                horizontal = 24.dp,
                                                vertical = 4.dp
                                            )
                                    )
                                }

                                if (programsList.size > 4) {
                                    item {
                                        Box(
                                            modifier =
                                                Modifier.fillMaxWidth()
                                                    .padding(horizontal = 24.dp),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            TextButton(
                                                onClick = {
                                                    isProgramsExpanded = !isProgramsExpanded
                                                }
                                            ) {
                                                Text(
                                                    text =
                                                        if (isProgramsExpanded) "Show Less"
                                                        else
                                                            "View All (${programsList.size})",
                                                    style = MaterialTheme.typography.labelLarge
                                                )
                                            }
                                        }
                                    }
                                }
                                item { Spacer(modifier = Modifier.height(32.dp)) }
                            }

                            if (detail.infrastructure.isNotEmpty()) {
                                item {
                                    NativeSectionHeader(title = "Infrastructure")
                                    Spacer(modifier = Modifier.height(16.dp))
                                    InfrastructureSection(
                                        infrastructure = detail.infrastructure,
                                        onAlbumClick = { selectedInfrastructure = it }
                                    )
                                    Spacer(modifier = Modifier.height(32.dp))
                                }
                            }

                            if (detail.gallery.isNotEmpty()) {
                                item {
                                    NativeSectionHeader(title = "Gallery")
                                    Spacer(modifier = Modifier.height(16.dp))
                                    GallerySection(
                                        gallery = detail.gallery,
                                        onAlbumClick = { selectedGallery = it }
                                    )
                                    Spacer(modifier = Modifier.height(32.dp))
                                }
                            }

                            if (detail.placement.isNotEmpty()) {
                                item {
                                    NativeSectionHeader(title = "Placement Cell")
                                    Spacer(modifier = Modifier.height(16.dp))
                                    LazyRow(
                                        contentPadding = PaddingValues(horizontal = 24.dp),
                                        horizontalArrangement = Arrangement.spacedBy(16.dp)
                                    ) {
                                        items(items = detail.placement) { member ->
                                            PlacementMemberCard(
                                                member = member,
                                                onImageLongClick = {
                                                    selectedProfileImage = it
                                                },
                                                onClick = { selectedPlacementMember = member }
                                            )
                                        }
                                    }
                                    Spacer(modifier = Modifier.height(32.dp))
                                }
                            }
                            if (detail.studentsRecruited.isNotEmpty()) {
                                item {
                                    NativeSectionHeader(title = "Students Recruited")
                                    Spacer(modifier = Modifier.height(16.dp))

                                    DepartmentStatisticsSection(
                                        studentsRecruited = detail.studentsRecruited,
                                        onDepartmentClick = { selectedStudentGroup = it }
                                    )
                                    Spacer(modifier = Modifier.height(32.dp))
                                }
                            }
                        }
                    }
                }

                if (state.error.isNotBlank()) {
                    ErrorState(message = state.error, modifier = Modifier.align(Alignment.Center))
                }

                if (state.isLoading) {
                    DepartmentDetailShimmer()
                }

                if (showBottomSheet) {
                    DepartmentDetailBottomSheet(
                        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
                        onDismissRequest = {
                            showBottomSheet = false
                            selectedInfrastructure = null
                            selectedGallery = null
                            selectedStudentGroup = null
                            selectedFaculty = null
                            selectedPlacementMember = null
                        },
                        selectedStudentGroup = selectedStudentGroup,
                        selectedFaculty = selectedFaculty,
                        selectedPlacementMember = selectedPlacementMember,
                        selectedInfrastructure = selectedInfrastructure,
                        selectedGallery = selectedGallery,
                        allStudentsRecruited = state.departmentDetail?.studentsRecruited ?: emptyList()
                    )
                }
            }
        }
        if (selectedProfileImage != null) {
            FullScreenProfileImage(
                imageUrl = selectedProfileImage!!,
                onDismiss = { selectedProfileImage = null }
            )
        }
    }
}
