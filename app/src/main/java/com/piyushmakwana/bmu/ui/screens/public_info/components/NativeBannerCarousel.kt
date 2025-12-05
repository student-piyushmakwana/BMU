package com.piyushmakwana.bmu.ui.screens.public_info.components

import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import coil3.compose.AsyncImage
import coil3.request.ImageRequest
import coil3.request.crossfade
import kotlinx.coroutines.delay

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun NativeBannerCarousel(banners: List<String>) {
    val pagerState = rememberPagerState(pageCount = { banners.size })

    LaunchedEffect(Unit) {
        while (true) {
            delay(5000)
            val nextPage = (pagerState.currentPage + 1) % banners.size
            pagerState.animateScrollToPage(
                page = nextPage,
                animationSpec = spring(stiffness = Spring.StiffnessLow)
            )
        }
    }

    Box(modifier = Modifier.fillMaxWidth().height(260.dp)) {
        HorizontalPager(state = pagerState, modifier = Modifier.fillMaxSize()) { page ->
            Box(modifier = Modifier.fillMaxSize()) {
                AsyncImage(
                    model =
                        ImageRequest.Builder(LocalContext.current)
                            .data(banners[page])
                            .crossfade(true)
                            .build(),
                    contentDescription = "Banner ${page + 1}",
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )

                Box(
                    modifier =
                        Modifier.fillMaxSize()
                            .background(
                                Brush.verticalGradient(
                                    colors =
                                        listOf(
                                            Color.Transparent,
                                            Color.Black.copy(
                                                alpha = 0.4f
                                            )
                                        ),
                                    startY = 300f
                                )
                            )
                )
            }
        }

        Row(
            modifier = Modifier.align(Alignment.BottomCenter).padding(bottom = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            repeat(banners.size) { index ->
                val isSelected = pagerState.currentPage == index
                val width by
                animateFloatAsState(
                    targetValue = if (isSelected) 24f else 8f,
                    animationSpec = tween(300)
                )
                Box(
                    modifier =
                        Modifier.height(6.dp)
                            .width(width.dp)
                            .clip(RoundedCornerShape(3.dp))
                            .background(
                                if (isSelected) MaterialTheme.colorScheme.primary
                                else Color.White.copy(alpha = 0.5f)
                            )
                )
            }
        }
    }
}