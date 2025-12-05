package com.piyushmakwana.bmu.ui.screens.public_info

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowForward
import androidx.compose.material.icons.rounded.KeyboardArrowUp
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.lifecycle.viewmodel.compose.hiltViewModel
import com.piyushmakwana.bmu.ui.screens.public_info.components.ErrorState
import com.piyushmakwana.bmu.ui.screens.public_info.components.NativeBannerCarousel
import com.piyushmakwana.bmu.ui.screens.public_info.components.NativeDepartmentCard
import com.piyushmakwana.bmu.ui.screens.public_info.components.NativeEventRow
import com.piyushmakwana.bmu.ui.screens.public_info.components.NativeNewsCard
import com.piyushmakwana.bmu.ui.screens.public_info.components.NativeSectionHeader
import com.piyushmakwana.bmu.ui.screens.public_info.components.NativeTestimonialCard
import com.piyushmakwana.bmu.ui.screens.public_info.components.NativeTopBar
import com.piyushmakwana.bmu.ui.screens.public_info.components.PublicInfoShimmer

@Composable
fun PublicInfoScreen(viewModel: PublicInfoViewModel = hiltViewModel()) {
    val state = viewModel.state.value
    var isEventsExpanded by remember { mutableStateOf(false) }
    val uriHandler = LocalUriHandler.current

    Scaffold(topBar = { NativeTopBar() }, containerColor = MaterialTheme.colorScheme.surface) {
            paddingValues ->
        Box(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
            if (state.publicInfo != null) {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 48.dp)
                ) {
                    item {
                        if (state.publicInfo.banners.isNotEmpty()) {
                            NativeBannerCarousel(
                                banners = state.publicInfo.banners
                            )
                            Spacer(modifier = Modifier.height(32.dp))
                        }
                    }

                    item {
                        if (state.publicInfo.latestNews.isNotEmpty()) {
                            NativeSectionHeader(
                                title = "Latest Updates"
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            LazyRow(
                                contentPadding =
                                    PaddingValues(
                                        horizontal = 24.dp
                                    ),
                                horizontalArrangement =
                                    Arrangement.spacedBy(16.dp)
                            ) {
                                items(state.publicInfo.latestNews) { news ->
                                    NativeNewsCard(
                                        news = news,
                                        onClick = { uriHandler.openUri(news.link) }
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.height(40.dp))
                        }
                    }

                    item {
                        if (state.publicInfo.upcomingEvents.isNotEmpty()) {
                            NativeSectionHeader(
                                title = "Upcoming Events"
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                        }
                    }

                    val events = state.publicInfo.upcomingEvents
                    val displayEvents =
                        if (isEventsExpanded) events else events.take(4)

                    items(displayEvents) {event -> NativeEventRow(
                        event = event,
                        onClick = {
                            uriHandler.openUri(event.link)
                        })
                    }

                    item {
                        if (events.size > 4) {
                            Box(
                                modifier =
                                    Modifier.fillMaxWidth()
                                        .padding(horizontal = 24.dp, vertical = 8.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Surface(
                                    onClick = { isEventsExpanded = !isEventsExpanded },
                                    shape = RoundedCornerShape(50),
                                    color =
                                        MaterialTheme.colorScheme.surfaceVariant.copy(
                                            alpha = 0.5f
                                        ),
                                    border =
                                        BorderStroke(
                                            1.dp,
                                            MaterialTheme.colorScheme.outlineVariant
                                                .copy(alpha = 0.5f)
                                        )
                                ) {
                                    Row(
                                        modifier =
                                            Modifier.padding(
                                                horizontal = 24.dp,
                                                vertical = 12.dp
                                            ),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            text =
                                                if (isEventsExpanded) "Show Less"
                                                else "View All Events",
                                            style = MaterialTheme.typography.labelLarge,
                                            fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.primary
                                        )
                                        Spacer(modifier = Modifier.width(8.dp))
                                        Icon(
                                            imageVector =
                                                if (isEventsExpanded)
                                                    Icons.Rounded.KeyboardArrowUp
                                                else
                                                    Icons.AutoMirrored.Rounded
                                                        .ArrowForward,
                                            contentDescription = null,
                                            tint = MaterialTheme.colorScheme.primary,
                                            modifier = Modifier.size(16.dp)
                                        )
                                    }
                                }
                            }
                        }

                        if (events.isNotEmpty()) {
                            Spacer(modifier = Modifier.height(40.dp))
                        }
                    }

                    item {
                        if (state.publicInfo.departments.isNotEmpty()) {
                            NativeSectionHeader(title = "Our Departments")
                            Spacer(modifier = Modifier.height(16.dp))
                            LazyRow(
                                contentPadding = PaddingValues(horizontal = 24.dp),
                                horizontalArrangement = Arrangement.spacedBy(16.dp)
                            ) {
                                items(state.publicInfo.departments) { department ->
                                    NativeDepartmentCard(department = department)
                                }
                            }
                            Spacer(modifier = Modifier.height(40.dp))
                        }
                    }

                    item {
                        if (state.publicInfo.testimonials.isNotEmpty()) {
                            NativeSectionHeader(
                                title = "Student Voices"
                            )
                            Spacer(modifier = Modifier.height(24.dp))
                            LazyRow(
                                contentPadding =
                                    PaddingValues(
                                        horizontal = 24.dp
                                    ),
                                horizontalArrangement =
                                    Arrangement.spacedBy(16.dp)
                            ) {
                                items(
                                    state.publicInfo
                                        .testimonials
                                ) { testimonial ->
                                    NativeTestimonialCard(
                                        testimonial
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.height(32.dp))
                        }
                    }
                }
            }

            if (state.error.isNotBlank()) {
                ErrorState(
                    message = state.error,
                    modifier = Modifier.align(Alignment.Center)
                )
            }

            if (state.isLoading) {
                PublicInfoShimmer()
            }
        }
    }
}