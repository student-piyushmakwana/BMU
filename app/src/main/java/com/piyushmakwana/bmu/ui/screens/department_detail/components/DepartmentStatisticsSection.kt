package com.piyushmakwana.bmu.ui.screens.department_detail.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.piyushmakwana.bmu.domain.model.StudentRecruited

@Composable
fun DepartmentStatisticsSection(
        studentsRecruited: List<StudentRecruited>,
        onDepartmentClick: (String) -> Unit
) {
    if (studentsRecruited.isNotEmpty()) {
        val departmentCounts =
                remember(studentsRecruited) {
                    studentsRecruited.groupingBy { it.departmentName }.eachCount()
                }

        val totalStudents = studentsRecruited.size
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
                            color = MaterialTheme.colorScheme.onSurfaceVariant
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
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                    text =
                            "This chart illustrates the distribution of recruited students across various departments, highlighting key placement areas.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    lineHeight = MaterialTheme.typography.bodySmall.lineHeight * 1.2
            )
        }
        Spacer(modifier = Modifier.height(24.dp))

        val colors =
                listOf(
                        MaterialTheme.colorScheme.primary.copy(alpha = 0.80f),
                        MaterialTheme.colorScheme.secondary.copy(alpha = 0.80f),
                        MaterialTheme.colorScheme.tertiary.copy(alpha = 0.80f),
                        MaterialTheme.colorScheme.error.copy(alpha = 0.80f),
                        MaterialTheme.colorScheme.primary.copy(alpha = 0.70f),
                        MaterialTheme.colorScheme.secondary.copy(alpha = 0.70f),
                        MaterialTheme.colorScheme.tertiary.copy(alpha = 0.70f),
                        MaterialTheme.colorScheme.error.copy(alpha = 0.70f),
                        MaterialTheme.colorScheme.primary.copy(alpha = 0.60f),
                        MaterialTheme.colorScheme.secondary.copy(alpha = 0.60f),
                        MaterialTheme.colorScheme.tertiary.copy(alpha = 0.60f),
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
                    onSliceClick = { department -> onDepartmentClick(department) }
            )
        }

        Column(modifier = Modifier.padding(horizontal = 24.dp)) {
            departmentCounts.entries.toList().forEachIndexed { index, (dept, count) ->
                val color = colors.getOrElse(index) { Color.Gray }
                val percentage = (count.toFloat() / totalStudents * 100).toInt()

                Card(
                        shape = RoundedCornerShape(8.dp),
                        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                        onClick = { onDepartmentClick(dept) }
                ) {
                    Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.padding(12.dp)
                    ) {
                        Box(modifier = Modifier.size(12.dp).clip(CircleShape).background(color))
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(
                                text = dept,
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurface,
                                modifier = Modifier.weight(1f)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                                text = "$percentage%",
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
        Spacer(modifier = Modifier.height(32.dp))
    }
}
