package com.piyushmakwana.bmu.ui.common.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay

@Composable
fun DetailRow(
    label: String,
    value: String,
    icon: ImageVector? = null,
    isCopyable: Boolean = false
) {
    if (value.isNotBlank()) {
        val clipboardManager = LocalClipboardManager.current
        var isCopied by remember { mutableStateOf(false) }

        LaunchedEffect(isCopied) {
            if (isCopied) {
                delay(2000)
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
