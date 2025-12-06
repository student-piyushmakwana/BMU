package com.piyushmakwana.bmu.ui.screens.department_detail.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Email
import androidx.compose.material.icons.rounded.Person
import androidx.compose.material.icons.rounded.Phone
import androidx.compose.material.icons.rounded.School
import androidx.compose.material.icons.rounded.Work
import androidx.compose.material3.Card
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.SheetState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.piyushmakwana.bmu.domain.model.Faculty
import com.piyushmakwana.bmu.domain.model.GalleryItem
import com.piyushmakwana.bmu.domain.model.InfrastructureItem
import com.piyushmakwana.bmu.domain.model.PlacementMember
import com.piyushmakwana.bmu.domain.model.StudentRecruited
import com.piyushmakwana.bmu.ui.common.ShimmerImage
import com.piyushmakwana.bmu.ui.common.components.DetailRow
import com.piyushmakwana.bmu.util.formatPhoneNumber

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DepartmentDetailBottomSheet(
        sheetState: SheetState,
        onDismissRequest: () -> Unit,
        selectedStudentGroup: String?,
        selectedFaculty: Faculty?,
        selectedPlacementMember: PlacementMember?,
        selectedInfrastructure: InfrastructureItem?,
        selectedGallery: GalleryItem?,
        allStudentsRecruited: List<StudentRecruited>
) {
    ModalBottomSheet(
            onDismissRequest = onDismissRequest,
            containerColor = MaterialTheme.colorScheme.surface,
            sheetState = sheetState
    ) {
        if (selectedStudentGroup != null) {
            val students = allStudentsRecruited.filter { it.departmentName == selectedStudentGroup }

            Column(modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp)) {
                Text(
                        text = selectedStudentGroup,
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(horizontal = 24.dp, vertical = 16.dp)
                )

                LazyColumn(
                        contentPadding = PaddingValues(horizontal = 24.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                        modifier = Modifier.height(400.dp)
                ) {
                    items(items = students) { student ->
                        StudentRecruitedRow(student = student, showDepartment = false)
                    }
                }
            }
        } else if (selectedFaculty != null) {
            val faculty = selectedFaculty
            Column(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Box(
                        modifier =
                                Modifier.size(120.dp)
                                        .clip(CircleShape)
                                        .background(MaterialTheme.colorScheme.surfaceVariant),
                        contentAlignment = Alignment.Center
                ) {
                    val isPhotoValid =
                            faculty.photo != null &&
                                    listOf(".jpg", ".jpeg", ".png", ".webp").any {
                                        faculty.photo.endsWith(it, ignoreCase = true)
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
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(horizontal = 24.dp)
                )

                Spacer(modifier = Modifier.height(8.dp))

                Text(
                        text = faculty.designation,
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.primary,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(horizontal = 24.dp)
                )

                Spacer(modifier = Modifier.height(24.dp))

                Column(
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
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
            val member = selectedPlacementMember
            Column(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Box(
                        modifier =
                                Modifier.size(120.dp)
                                        .clip(CircleShape)
                                        .background(MaterialTheme.colorScheme.surfaceVariant),
                        contentAlignment = Alignment.Center
                ) {
                    val isPhotoValid =
                            member.photo != null &&
                                    listOf(".jpg", ".jpeg", ".png", ".webp").any {
                                        member.photo.endsWith(it, ignoreCase = true)
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
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(horizontal = 24.dp)
                )

                Spacer(modifier = Modifier.height(8.dp))

                Text(
                        text = member.designation,
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.primary,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(horizontal = 24.dp)
                )

                Spacer(modifier = Modifier.height(24.dp))

                Column(
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
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
            val title = selectedInfrastructure?.title ?: selectedGallery?.title ?: ""
            val images = selectedInfrastructure?.images ?: selectedGallery?.images ?: emptyList()

            Column(modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp)) {
                Text(
                        text = title,
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.padding(horizontal = 24.dp, vertical = 16.dp)
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
