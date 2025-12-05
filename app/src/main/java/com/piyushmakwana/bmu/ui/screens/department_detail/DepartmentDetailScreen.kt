package com.piyushmakwana.bmu.ui.screens.department_detail

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import com.piyushmakwana.bmu.domain.model.GalleryItem
import com.piyushmakwana.bmu.domain.model.InfrastructureItem
import com.piyushmakwana.bmu.ui.common.ShimmerImage
import com.piyushmakwana.bmu.ui.screens.department_detail.components.DepartmentDetailShimmer
import com.piyushmakwana.bmu.ui.screens.department_detail.components.DirectorCard
import com.piyushmakwana.bmu.ui.screens.department_detail.components.FacultyCard
import com.piyushmakwana.bmu.ui.screens.department_detail.components.GallerySection
import com.piyushmakwana.bmu.ui.screens.department_detail.components.InfrastructureSection
import com.piyushmakwana.bmu.ui.screens.department_detail.components.PlacementMemberCard
import com.piyushmakwana.bmu.ui.screens.department_detail.components.ProgramSection
import com.piyushmakwana.bmu.ui.screens.department_detail.components.StudentRecruitedRow
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
    var showBottomSheet by remember { mutableStateOf(false) }

    if (selectedInfrastructure != null || selectedGallery != null) {
        showBottomSheet = true
    }

    Scaffold(
        topBar = {
            NativeBackTopBar(
                title = state.departmentDetail?.name ?: "Department Details",
                onBackClick = { navController.popBackStack() }
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { paddingValues ->
        Box(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
            if (state.departmentDetail != null) {
                val detail = state.departmentDetail
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 48.dp)
                ) {
                    item { Spacer(modifier = Modifier.height(16.dp)) }

                    item {
                        NativeSectionHeader(title = "Director")
                        Spacer(modifier = Modifier.height(16.dp))
                        DirectorCard(
                            director = detail.director,
                            modifier = Modifier.padding(horizontal = 24.dp)
                        )
                        Spacer(modifier = Modifier.height(32.dp))
                    }

                    if (detail.faculty.isNotEmpty()) {
                        item {
                            NativeSectionHeader(title = "Faculty Members")
                            Spacer(modifier = Modifier.height(16.dp))
                            LazyRow(
                                contentPadding = PaddingValues(horizontal = 24.dp),
                                horizontalArrangement = Arrangement.spacedBy(16.dp)
                            ) {
                                items(detail.faculty) { faculty -> FacultyCard(faculty = faculty) }
                            }
                            Spacer(modifier = Modifier.height(32.dp))
                        }
                    }

                    if (detail.programs.isNotEmpty()) {
                        item {
                            NativeSectionHeader(title = "Programs Offered")
                            Spacer(modifier = Modifier.height(16.dp))
                        }
                        items(detail.programs.entries.toList()) { (name, program) ->
                            ProgramSection(
                                programName = name,
                                program = program,
                                modifier = Modifier.padding(horizontal = 24.dp, vertical = 4.dp)
                            )
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
                                items(detail.placement) { member ->
                                    PlacementMemberCard(member = member)
                                }
                            }
                            Spacer(modifier = Modifier.height(32.dp))
                        }
                    }

                    if (detail.studentsRecruited.isNotEmpty()) {
                        item {
                            NativeSectionHeader(title = "Students Recruited")
                            Spacer(modifier = Modifier.height(16.dp))
                        }
                        items(detail.studentsRecruited.take(20)) { student ->
                            StudentRecruitedRow(
                                student = student,
                                modifier = Modifier.padding(horizontal = 24.dp, vertical = 4.dp)
                            )
                        }
                        if (detail.studentsRecruited.size > 20) {
                            item {
                                Text(
                                    text =
                                        "+${detail.studentsRecruited.size - 20} more students placed",
                                    style = MaterialTheme.typography.labelMedium,
                                    color = MaterialTheme.colorScheme.primary,
                                    fontWeight = FontWeight.Bold,
                                    modifier =
                                        Modifier.padding(
                                            horizontal = 24.dp,
                                            vertical = 8.dp
                                        )
                                )
                            }
                        }
                        item { Spacer(modifier = Modifier.height(32.dp)) }
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
                ModalBottomSheet(
                    onDismissRequest = {
                        showBottomSheet = false
                        selectedInfrastructure = null
                        selectedGallery = null
                    },
                    containerColor = MaterialTheme.colorScheme.surface,
                    sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
                ) {
                    val title = selectedInfrastructure?.title ?: selectedGallery?.title ?: ""
                    val images =
                        selectedInfrastructure?.images ?: selectedGallery?.images ?: emptyList()

                    Column(modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp)) {
                        Text(
                            text = title,
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(horizontal = 24.dp, vertical = 16.dp)
                        )

                        LazyVerticalGrid(
                            columns = GridCells.Fixed(2),
                            contentPadding = PaddingValues(horizontal = 24.dp),
                            horizontalArrangement = Arrangement.spacedBy(12.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items(images) { imageUrl ->
                                Card(
                                    shape = RoundedCornerShape(12.dp),
                                    modifier = Modifier.aspectRatio(1f)
                                ) {
                                    ShimmerImage(
                                        model = imageUrl,
                                        contentDescription = null,
                                        modifier = Modifier.fillMaxSize(),
                                        contentScale = ContentScale.Crop
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}