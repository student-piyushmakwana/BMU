package com.piyushmakwana.bmu.ui.screens.department_detail

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Apartment
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
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
import androidx.compose.ui.draw.blur
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.lifecycle.viewmodel.compose.hiltViewModel
import androidx.navigation.NavController
import com.piyushmakwana.bmu.domain.model.GalleryItem
import com.piyushmakwana.bmu.domain.model.InfrastructureItem
import com.piyushmakwana.bmu.ui.common.ShimmerImage
import com.piyushmakwana.bmu.ui.screens.department_detail.components.DepartmentDetailShimmer
import com.piyushmakwana.bmu.ui.screens.department_detail.components.DirectorCard
import com.piyushmakwana.bmu.ui.screens.department_detail.components.FacultyCard
import com.piyushmakwana.bmu.ui.screens.department_detail.components.FullScreenProfileImage
import com.piyushmakwana.bmu.ui.screens.department_detail.components.GallerySection
import com.piyushmakwana.bmu.ui.screens.department_detail.components.InfrastructureSection
import com.piyushmakwana.bmu.ui.screens.department_detail.components.PieChart
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
    var selectedStudentGroup by remember { mutableStateOf<String?>(null) }
    var selectedProfileImage by remember { mutableStateOf<String?>(null) }
    var showBottomSheet by remember { mutableStateOf(false) }

    if (selectedInfrastructure != null || selectedGallery != null || selectedStudentGroup != null) {
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
                            Card(
                                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                                colors =
                                    CardDefaults.cardColors(
                                        containerColor =
                                            MaterialTheme.colorScheme.surfaceVariant
                                                .copy(alpha = 0.5f)
                                    ),
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Row(
                                    modifier = Modifier.padding(16.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        imageVector = Icons.Rounded.Apartment,
                                        contentDescription = null,
                                        tint = MaterialTheme.colorScheme.primary,
                                        modifier = Modifier.size(24.dp)
                                    )
                                    Spacer(modifier = Modifier.width(16.dp))
                                    Text(
                                        text = detail.name,
                                        style = MaterialTheme.typography.titleMedium,
                                        fontWeight = FontWeight.SemiBold,
                                        color = MaterialTheme.colorScheme.onSurface
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.height(32.dp))
                        }

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
                                            onImageLongClick = { selectedProfileImage = it }
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

                            items(items = programsList, key = { it.key }) { (name, program) ->
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
                                            onImageLongClick = { selectedProfileImage = it }
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

                                val departmentCounts =
                                    remember(detail.studentsRecruited) {
                                        detail.studentsRecruited
                                            .groupingBy { it.departmentName }
                                            .eachCount()
                                    }

                                val totalStudents = detail.studentsRecruited.size
                                val totalDepartments = departmentCounts.size

                                Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceAround
                                    ) {
                                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                            Text(
                                                text = "$totalStudents",
                                                style = MaterialTheme.typography.headlineMedium,
                                                fontWeight = FontWeight.Bold,
                                                color = MaterialTheme.colorScheme.primary
                                            )
                                            Text(
                                                text = "Total Students",
                                                style = MaterialTheme.typography.labelMedium,
                                                color =
                                                    MaterialTheme.colorScheme
                                                        .onSurfaceVariant
                                            )
                                        }
                                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                            Text(
                                                text = "$totalDepartments",
                                                style = MaterialTheme.typography.headlineMedium,
                                                fontWeight = FontWeight.Bold,
                                                color = MaterialTheme.colorScheme.secondary
                                            )
                                            Text(
                                                text = "Departments",
                                                style = MaterialTheme.typography.labelMedium,
                                                color =
                                                    MaterialTheme.colorScheme
                                                        .onSurfaceVariant
                                            )
                                        }
                                    }
                                    Spacer(modifier = Modifier.height(16.dp))
                                    Text(
                                        text =
                                            "This chart illustrates the distribution of recruited students across various departments, highlighting key placement areas.",
                                        style = MaterialTheme.typography.bodySmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        lineHeight =
                                            MaterialTheme.typography.bodySmall.lineHeight *
                                                    1.2
                                    )
                                }
                                Spacer(modifier = Modifier.height(24.dp))

                                val colors =
                                    listOf(
                                        MaterialTheme.colorScheme.primary.copy(
                                            alpha = 0.80f
                                        ),
                                        MaterialTheme.colorScheme.secondary.copy(
                                            alpha = 0.80f
                                        ),
                                        MaterialTheme.colorScheme.tertiary.copy(
                                            alpha = 0.80f
                                        ),
                                        MaterialTheme.colorScheme.error.copy(alpha = 0.80f),
                                        MaterialTheme.colorScheme.primary.copy(
                                            alpha = 0.70f
                                        ),
                                        MaterialTheme.colorScheme.secondary.copy(
                                            alpha = 0.70f
                                        ),
                                        MaterialTheme.colorScheme.tertiary.copy(
                                            alpha = 0.70f
                                        ),
                                        MaterialTheme.colorScheme.error.copy(alpha = 0.70f),
                                        MaterialTheme.colorScheme.primary.copy(
                                            alpha = 0.60f
                                        ),
                                        MaterialTheme.colorScheme.secondary.copy(
                                            alpha = 0.60f
                                        ),
                                        MaterialTheme.colorScheme.tertiary.copy(
                                            alpha = 0.60f
                                        ),
                                        MaterialTheme.colorScheme.error.copy(alpha = 0.60f)
                                    )

                                Box(
                                    modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp),
                                    contentAlignment = Alignment.Center
                                ) {
                                    PieChart(
                                        data = departmentCounts,
                                        colors = colors,
                                        radiusOuter = 100.dp,
                                        onSliceClick = { department ->
                                            selectedStudentGroup = department
                                        }
                                    )
                                }

                                Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                                    departmentCounts.entries.toList().forEachIndexed {
                                            index,
                                            (dept, count) ->
                                        val color = colors.getOrElse(index) { Color.Gray }
                                        val percentage =
                                            (count.toFloat() / totalStudents * 100).toInt()

                                        Card(
                                            shape = RoundedCornerShape(8.dp),
                                            modifier =
                                                Modifier.fillMaxWidth()
                                                    .padding(vertical = 4.dp),
                                            onClick = { selectedStudentGroup = dept }
                                        ) {
                                            Row(
                                                verticalAlignment = Alignment.CenterVertically,
                                                modifier = Modifier.padding(12.dp)
                                            ) {
                                                Box(
                                                    modifier =
                                                        Modifier.size(12.dp)
                                                            .clip(CircleShape)
                                                            .background(color)
                                                )
                                                Spacer(modifier = Modifier.width(12.dp))
                                                Text(
                                                    text = dept,
                                                    style = MaterialTheme.typography.bodyMedium,
                                                    color = MaterialTheme.colorScheme.onSurface,
                                                    modifier = Modifier.weight(1f)
                                                )
                                                Text(
                                                    text = "$percentage%",
                                                    style = MaterialTheme.typography.bodyMedium,
                                                    fontWeight = FontWeight.Bold,
                                                    color =
                                                        MaterialTheme.colorScheme
                                                            .onSurfaceVariant
                                                )
                                            }
                                        }
                                    }
                                }
                                Spacer(modifier = Modifier.height(32.dp))
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
                    ModalBottomSheet(
                        onDismissRequest = {
                            showBottomSheet = false
                            selectedInfrastructure = null
                            selectedGallery = null
                            selectedStudentGroup = null
                        },
                        containerColor = MaterialTheme.colorScheme.surface,
                        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
                    ) {
                        if (selectedStudentGroup != null) {
                            val students =
                                state.departmentDetail?.studentsRecruited?.filter {
                                    it.departmentName == selectedStudentGroup
                                }
                                    ?: emptyList()

                            Column(modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp)) {
                                Text(
                                    text = selectedStudentGroup ?: "",
                                    style = MaterialTheme.typography.titleLarge,
                                    fontWeight = FontWeight.Bold,
                                    modifier =
                                        Modifier.padding(
                                            horizontal = 24.dp,
                                            vertical = 16.dp
                                        )
                                )

                                LazyColumn(
                                    contentPadding = PaddingValues(horizontal = 24.dp),
                                    verticalArrangement = Arrangement.spacedBy(8.dp),
                                    modifier = Modifier.height(400.dp)
                                ) {
                                    items(items = students) { student ->
                                        StudentRecruitedRow(
                                            student = student,
                                            showDepartment = false
                                        )
                                    }
                                }
                            }
                        } else {
                            val title =
                                selectedInfrastructure?.title ?: selectedGallery?.title ?: ""
                            val images =
                                selectedInfrastructure?.images
                                    ?: selectedGallery?.images ?: emptyList()

                            Column(modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp)) {
                                Text(
                                    text = title,
                                    style = MaterialTheme.typography.titleLarge,
                                    fontWeight = FontWeight.Bold,
                                    modifier =
                                        Modifier.padding(
                                            horizontal = 24.dp,
                                            vertical = 16.dp
                                        )
                                )

                                LazyVerticalGrid(
                                    columns = GridCells.Fixed(2),
                                    contentPadding = PaddingValues(horizontal = 24.dp),
                                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                                    verticalArrangement = Arrangement.spacedBy(12.dp)
                                ) {
                                    items(items = images, key = { it }) { imageUrl ->
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
        if (selectedProfileImage != null) {
            FullScreenProfileImage(
                imageUrl = selectedProfileImage!!,
                onDismiss = { selectedProfileImage = null }
            )
        }
    }
}