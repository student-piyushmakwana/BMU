package com.piyushmakwana.bmu.ui.screens.department_detail.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.piyushmakwana.bmu.ui.common.shimmerEffect

@Composable
fun DepartmentDetailShimmer() {
    LazyColumn(modifier = Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 48.dp)) {
        item {
            Column(modifier = Modifier.padding(24.dp)) {
                Box(
                    modifier =
                        Modifier.width(120.dp)
                            .height(24.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(16.dp))
                Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.Top) {
                    Box(
                        modifier =
                            Modifier.size(100.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .shimmerEffect()
                    )
                    Spacer(modifier = Modifier.width(16.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Box(
                            modifier =
                                Modifier.fillMaxWidth()
                                    .height(20.dp)
                                    .clip(RoundedCornerShape(4.dp))
                                    .shimmerEffect()
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Box(
                            modifier =
                                Modifier.width(150.dp)
                                    .height(16.dp)
                                    .clip(RoundedCornerShape(4.dp))
                                    .shimmerEffect()
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Box(
                            modifier =
                                Modifier.fillMaxWidth()
                                    .height(60.dp)
                                    .clip(RoundedCornerShape(4.dp))
                                    .shimmerEffect()
                        )
                    }
                }
            }
        }

        item {
            Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                Box(
                    modifier =
                        Modifier.width(100.dp)
                            .height(24.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(16.dp))
            }
            LazyRow(
                contentPadding = PaddingValues(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(4) {
                    Box(
                        modifier =
                            Modifier.width(140.dp)
                                .height(180.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .shimmerEffect()
                    )
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
        }

        item {
            Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                Box(
                    modifier =
                        Modifier.width(120.dp)
                            .height(24.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(16.dp))
                repeat(3) {
                    Box(
                        modifier =
                            Modifier.fillMaxWidth()
                                .height(56.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .shimmerEffect()
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
        }

        item {
            Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                Box(
                    modifier =
                        Modifier.width(80.dp)
                            .height(24.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(16.dp))
            }
            LazyRow(
                contentPadding = PaddingValues(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(3) {
                    Box(
                        modifier =
                            Modifier.width(200.dp)
                                .height(150.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .shimmerEffect()
                    )
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
        }

        item {
            Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                Box(
                    modifier =
                        Modifier.width(130.dp)
                            .height(24.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(16.dp))
            }
            LazyRow(
                contentPadding = PaddingValues(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(3) {
                    Box(
                        modifier =
                            Modifier.width(200.dp)
                                .height(150.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .shimmerEffect()
                    )
                }
            }
        }
    }
}