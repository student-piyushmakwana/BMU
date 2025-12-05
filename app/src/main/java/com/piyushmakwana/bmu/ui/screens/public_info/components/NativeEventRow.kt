package com.piyushmakwana.bmu.ui.screens.public_info.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.piyushmakwana.bmu.domain.model.UpcomingEventItem

@Composable
fun NativeEventRow(event: UpcomingEventItem, onClick: () -> Unit) {
    Card(
        onClick = onClick,
        colors =
            CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        shape = RoundedCornerShape(0.dp)
    ) {
        Row(
            modifier =
                Modifier.fillMaxWidth()
                    .padding(horizontal = 24.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Card(
                colors =
                    CardDefaults.cardColors(
                        containerColor =
                            MaterialTheme.colorScheme.primaryContainer
                    ),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.size(60.dp)
            ) {
                Column(
                    modifier = Modifier.fillMaxSize(),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    val dateParts = event.date.split("/")
                    if (dateParts.size >= 2) {
                        Text(
                            text = dateParts[0],
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.Bold,
                            color =
                                MaterialTheme.colorScheme
                                    .onPrimaryContainer
                        )
                        Text(
                            text = getMonthName(dateParts[1]),
                            style = MaterialTheme.typography.labelSmall,
                            fontWeight = FontWeight.Bold,
                            color =
                                MaterialTheme.colorScheme
                                    .onPrimaryContainer.copy(
                                        alpha = 0.7f
                                    )
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = event.description,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.SemiBold,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "Tap for details",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}

fun getMonthName(month: String): String {
    return when (month.toIntOrNull()) {
        1 -> "JAN"
        2 -> "FEB"
        3 -> "MAR"
        4 -> "APR"
        5 -> "MAY"
        6 -> "JUN"
        7 -> "JUL"
        8 -> "AUG"
        9 -> "SEP"
        10 -> "OCT"
        11 -> "NOV"
        12 -> "DEC"
        else -> month
    }
}