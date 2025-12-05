package com.piyushmakwana.bmu.ui.screens.public_info.components

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
fun PublicInfoShimmer() {
    LazyColumn(modifier = Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 48.dp)) {
        item {
            Box(modifier = Modifier.fillMaxWidth().height(260.dp).shimmerEffect())
            Spacer(modifier = Modifier.height(32.dp))
        }

        item {
            Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                Box(
                    modifier =
                        Modifier.width(150.dp)
                            .height(24.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(16.dp))
            }
            LazyRow(
                contentPadding = PaddingValues(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(3) {
                    Box(
                        modifier =
                            Modifier.width(280.dp)
                                .height(180.dp)
                                .clip(RoundedCornerShape(16.dp))
                                .shimmerEffect()
                    )
                }
            }
            Spacer(modifier = Modifier.height(40.dp))
        }

        item {
            Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                Box(
                    modifier =
                        Modifier.width(180.dp)
                            .height(24.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(16.dp))
            }
        }

        items(4) {
            Row(
                modifier =
                    Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(modifier = Modifier.size(60.dp).clip(RoundedCornerShape(12.dp)).shimmerEffect())
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
                            Modifier.width(100.dp)
                                .height(16.dp)
                                .clip(RoundedCornerShape(4.dp))
                                .shimmerEffect()
                    )
                }
            }
        }

        item { Spacer(modifier = Modifier.height(40.dp)) }

        item {
            Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                Box(
                    modifier =
                        Modifier.width(160.dp)
                            .height(24.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(24.dp))
            }
            LazyRow(
                contentPadding = PaddingValues(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(3) {
                    Box(
                        modifier =
                            Modifier.width(280.dp)
                                .height(120.dp)
                                .clip(RoundedCornerShape(16.dp))
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
                        Modifier.width(160.dp)
                            .height(24.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(24.dp))
            }
            LazyRow(
                contentPadding = PaddingValues(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(3) {
                    Box(
                        modifier =
                            Modifier.width(300.dp)
                                .height(360.dp)
                                .clip(RoundedCornerShape(16.dp))
                                .shimmerEffect()
                    )
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}