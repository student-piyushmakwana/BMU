package com.piyushmakwana.bmu.ui.screens.department_detail

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.material.icons.rounded.Email
import androidx.compose.material.icons.rounded.HourglassEmpty
import androidx.compose.material.icons.rounded.Person
import androidx.compose.material.icons.rounded.Phone
import androidx.compose.material.icons.rounded.School
import androidx.compose.material.icons.rounded.Work
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.blur
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.AnnotatedString
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
                                Column(
                                    modifier =
                                        Modifier.fillMaxWidth()
                                            .fillParentMaxHeight(0.7f)
                                            .padding(horizontal = 24.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally,
                                    verticalArrangement = Arrangement.Center
                                ) {
                                    Icon(
                                        imageVector = Icons.Rounded.HourglassEmpty,
                                        contentDescription = null,
                                        modifier = Modifier.size(64.dp),
                                        tint =
                                            MaterialTheme.colorScheme.onSurfaceVariant.copy(
                                                alpha = 0.5f
                                            )
                                    )
                                    Spacer(modifier = Modifier.height(16.dp))
                                    Text(
                                        text =
                                            "Data for this department is currently unavailable.",
                                        style = MaterialTheme.typography.bodyLarge,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        fontWeight = FontWeight.Medium,
                                        textAlign =
                                            androidx.compose.ui.text.style.TextAlign.Center
                                    )
                                }
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
                                            Column(
                                                horizontalAlignment =
                                                    Alignment.CenterHorizontally
                                            ) {
                                                Text(
                                                    text = "$totalStudents",
                                                    style =
                                                        MaterialTheme.typography
                                                            .headlineMedium,
                                                    fontWeight = FontWeight.Bold,
                                                    color = MaterialTheme.colorScheme.primary
                                                )
                                                Text(
                                                    text = "Total Students",
                                                    style =
                                                        MaterialTheme.typography
                                                            .labelMedium,
                                                    color =
                                                        MaterialTheme.colorScheme
                                                            .onSurfaceVariant
                                                )
                                            }
                                            Column(
                                                horizontalAlignment =
                                                    Alignment.CenterHorizontally
                                            ) {
                                                Text(
                                                    text = "$totalDepartments",
                                                    style =
                                                        MaterialTheme.typography
                                                            .headlineMedium,
                                                    fontWeight = FontWeight.Bold,
                                                    color = MaterialTheme.colorScheme.secondary
                                                )
                                                Text(
                                                    text = "Departments",
                                                    style =
                                                        MaterialTheme.typography
                                                            .labelMedium,
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
                                                MaterialTheme.typography
                                                    .bodySmall
                                                    .lineHeight * 1.2
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
                                            MaterialTheme.colorScheme.error.copy(
                                                alpha = 0.80f
                                            ),
                                            MaterialTheme.colorScheme.primary.copy(
                                                alpha = 0.70f
                                            ),
                                            MaterialTheme.colorScheme.secondary.copy(
                                                alpha = 0.70f
                                            ),
                                            MaterialTheme.colorScheme.tertiary.copy(
                                                alpha = 0.70f
                                            ),
                                            MaterialTheme.colorScheme.error.copy(
                                                alpha = 0.70f
                                            ),
                                            MaterialTheme.colorScheme.primary.copy(
                                                alpha = 0.60f
                                            ),
                                            MaterialTheme.colorScheme.secondary.copy(
                                                alpha = 0.60f
                                            ),
                                            MaterialTheme.colorScheme.tertiary.copy(
                                                alpha = 0.60f
                                            ),
                                            MaterialTheme.colorScheme.error.copy(
                                                alpha = 0.60f
                                            )
                                        )

                                    Box(
                                        modifier =
                                            Modifier.fillMaxWidth().padding(bottom = 24.dp),
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
                                                    verticalAlignment =
                                                        Alignment.CenterVertically,
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
                                                        style =
                                                            MaterialTheme.typography
                                                                .bodyMedium,
                                                        color =
                                                            MaterialTheme.colorScheme
                                                                .onSurface,
                                                        modifier = Modifier.weight(1f)
                                                    )
                                                    Text(
                                                        text = "$percentage%",
                                                        style =
                                                            MaterialTheme.typography
                                                                .bodyMedium,
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
                            selectedFaculty = null
                            selectedPlacementMember = null
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
                        } else if (selectedFaculty != null) {
                            val faculty = selectedFaculty!!
                            Column(
                                modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Box(
                                    modifier =
                                        Modifier.size(120.dp)
                                            .clip(CircleShape)
                                            .background(
                                                MaterialTheme.colorScheme
                                                    .surfaceVariant
                                            ),
                                    contentAlignment = Alignment.Center
                                ) {
                                    val isPhotoValid =
                                        faculty.photo != null &&
                                                listOf(".jpg", ".jpeg", ".png", ".webp").any {
                                                    faculty.photo.endsWith(
                                                        it,
                                                        ignoreCase = true
                                                    )
                                                }
                                    if (isPhotoValid) {
                                        ShimmerImage(
                                            model = faculty.photo,
                                            contentDescription = faculty.name,
                                            modifier = Modifier.fillMaxSize(),
                                            contentScale = ContentScale.Crop
                                        )
                                    } else {
                                        Icon(
                                            imageVector = Icons.Rounded.Person,
                                            contentDescription = null,
                                            modifier = Modifier.size(64.dp),
                                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                    }
                                }

                                Spacer(modifier = Modifier.height(16.dp))

                                Text(
                                    text = faculty.name,
                                    style = MaterialTheme.typography.headlineSmall,
                                    fontWeight = FontWeight.Bold,
                                    textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                                    modifier = Modifier.padding(horizontal = 24.dp)
                                )

                                Spacer(modifier = Modifier.height(8.dp))

                                Text(
                                    text = faculty.designation,
                                    style = MaterialTheme.typography.titleMedium,
                                    color = MaterialTheme.colorScheme.primary,
                                    textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                                    modifier = Modifier.padding(horizontal = 24.dp)
                                )

                                Spacer(modifier = Modifier.height(24.dp))

                                Column(
                                    modifier =
                                        Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                                    verticalArrangement = Arrangement.spacedBy(12.dp)
                                ) {
                                    if (!faculty.qualification.isNullOrBlank()) {
                                        DetailRow(
                                            label = "Qualification",
                                            value = faculty.qualification,
                                            icon = Icons.Rounded.School
                                        )
                                    }
                                    DetailRow(
                                        label = "Specialization",
                                        value = faculty.specialization,
                                        icon = Icons.Rounded.Work
                                    )
                                    DetailRow(
                                        label = "Email",
                                        value = faculty.email,
                                        icon = Icons.Rounded.Email,
                                        isCopyable = true
                                    )
                                }
                            }
                        } else if (selectedPlacementMember != null) {
                            val member = selectedPlacementMember!!
                            Column(
                                modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Box(
                                    modifier =
                                        Modifier.size(120.dp)
                                            .clip(CircleShape)
                                            .background(
                                                MaterialTheme.colorScheme
                                                    .surfaceVariant
                                            ),
                                    contentAlignment = Alignment.Center
                                ) {
                                    val isPhotoValid =
                                        member.photo != null &&
                                                listOf(".jpg", ".jpeg", ".png", ".webp").any {
                                                    member.photo.endsWith(
                                                        it,
                                                        ignoreCase = true
                                                    )
                                                }
                                    if (isPhotoValid) {
                                        ShimmerImage(
                                            model = member.photo,
                                            contentDescription = member.name,
                                            modifier = Modifier.fillMaxSize(),
                                            contentScale = ContentScale.Crop
                                        )
                                    } else {
                                        Icon(
                                            imageVector = Icons.Rounded.Person,
                                            contentDescription = null,
                                            modifier = Modifier.size(64.dp),
                                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                    }
                                }

                                Spacer(modifier = Modifier.height(16.dp))

                                Text(
                                    text = member.name,
                                    style = MaterialTheme.typography.headlineSmall,
                                    fontWeight = FontWeight.Bold,
                                    textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                                    modifier = Modifier.padding(horizontal = 24.dp)
                                )

                                Spacer(modifier = Modifier.height(8.dp))

                                Text(
                                    text = member.designation,
                                    style = MaterialTheme.typography.titleMedium,
                                    color = MaterialTheme.colorScheme.primary,
                                    textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                                    modifier = Modifier.padding(horizontal = 24.dp)
                                )

                                Spacer(modifier = Modifier.height(24.dp))

                                Column(
                                    modifier =
                                        Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                                    verticalArrangement = Arrangement.spacedBy(12.dp)
                                ) {
                                    DetailRow(
                                        label = "Qualification",
                                        value = member.qualification,
                                        icon = Icons.Rounded.School
                                    )
                                    DetailRow(
                                        label = "Email",
                                        value = member.email,
                                        icon = Icons.Rounded.Email,
                                        isCopyable = true
                                    )
                                    if (member.phone.isNotBlank()) {
                                        DetailRow(
                                            label = "Phone",
                                            value = formatPhoneNumber(member.phone),
                                            icon = Icons.Rounded.Phone,
                                            isCopyable = true
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
                                    maxLines = 2,
                                    overflow =
                                        androidx.compose.ui.text.style.TextOverflow
                                            .Ellipsis,
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

@Composable
fun DetailRow(
    label: String,
    value: String,
    icon: ImageVector? = null,
    isCopyable: Boolean = false
) {
    if (value.isNotBlank()) {
        val clipboardManager = androidx.compose.ui.platform.LocalClipboardManager.current
        var isCopied by remember { mutableStateOf(false) }

        LaunchedEffect(isCopied) {
            if (isCopied) {
                kotlinx.coroutines.delay(2000)
                isCopied = false
            }
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            if (icon != null) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp).padding(top = 2.dp)
                )
            } else {
                Spacer(modifier = Modifier.size(20.dp))
            }

            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    text = label,
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(
                        text = value,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurface,
                        fontWeight = FontWeight.Medium
                    )
                    if (isCopyable) {
                        Box(
                            modifier =
                                Modifier.clip(RoundedCornerShape(4.dp))
                                    .background(
                                        if (isCopied)
                                            MaterialTheme.colorScheme
                                                .primaryContainer
                                        else
                                            MaterialTheme.colorScheme
                                                .surfaceVariant
                                    )
                                    .clickable {
                                        clipboardManager.setText(AnnotatedString(value))
                                        isCopied = true
                                    }
                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                        ) {
                            Text(
                                text = if (isCopied) "Copied!" else "Copy",
                                style = MaterialTheme.typography.labelSmall,
                                color =
                                    if (isCopied)
                                        MaterialTheme.colorScheme.onPrimaryContainer
                                    else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }
}

private fun formatPhoneNumber(phone: String): String {
    val cleaned = phone.replace("+91", "").replace(" ", "")
    return if (cleaned.length == 10) {
        "${cleaned.take(5)} ${cleaned.substring(5)}"
    } else {
        cleaned
    }
}