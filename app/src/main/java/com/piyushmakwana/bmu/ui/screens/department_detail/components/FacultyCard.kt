package com.piyushmakwana.bmu.ui.screens.department_detail.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.piyushmakwana.bmu.domain.model.Faculty
import com.piyushmakwana.bmu.ui.common.ShimmerImage

@Composable
fun FacultyCard(faculty: Faculty, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.width(150.dp).height(220.dp),
        shape = RoundedCornerShape(16.dp),
        colors =
            CardDefaults.cardColors(
                containerColor =
                    MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
            )
    ) {
        Column(
            modifier = Modifier.fillMaxWidth().padding(12.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Box(
                modifier =
                    Modifier.size(88.dp)
                        .clip(CircleShape)
                        .background(
                            Brush.linearGradient(
                                colors =
                                    listOf(
                                        MaterialTheme
                                            .colorScheme
                                            .primary
                                            .copy(
                                                alpha =
                                                    0.3f
                                            ),
                                        MaterialTheme
                                            .colorScheme
                                            .tertiary
                                            .copy(
                                                alpha =
                                                    0.3f
                                            )
                                    )
                            )
                        )
                        .padding(3.dp),
                contentAlignment = Alignment.Center
            ) {
                ShimmerImage(
                    model = faculty.photo,
                    contentDescription = faculty.name,
                    modifier = Modifier.size(82.dp).clip(CircleShape),
                    contentScale = ContentScale.Crop
                )
            }

            Spacer(modifier = Modifier.height(12.dp))

            Text(
                text = faculty.name,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                textAlign = TextAlign.Center,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = faculty.designation,
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.weight(1f))

            Box(
                modifier =
                    Modifier.clip(RoundedCornerShape(8.dp))
                        .background(
                            MaterialTheme.colorScheme.primary.copy(
                                alpha = 0.1f
                            )
                        )
                        .padding(horizontal = 8.dp, vertical = 4.dp)
            ) {
                Text(
                    text = faculty.specialization,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.Medium,
                    textAlign = TextAlign.Center,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}