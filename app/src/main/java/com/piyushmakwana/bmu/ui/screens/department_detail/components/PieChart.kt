package com.piyushmakwana.bmu.ui.screens.department_detail.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.toSize
import kotlin.math.atan2

@Composable
fun PieChart(
    data: Map<String, Int>,
    colors: List<Color>,
    modifier: Modifier = Modifier,
    radiusOuter: Dp = 100.dp,
    onSliceClick: (String) -> Unit
) {
    if (data.isEmpty()) return

    val totalSum = data.values.sum()
    val sweepAngles = remember(data) {
        val angles = mutableListOf<Float>()
        data.values.forEach {
            angles.add(360f * it / totalSum)
        }
        angles
    }

    val keys = data.keys.toList()

    Canvas(
        modifier = modifier
            .size(radiusOuter * 2f)
            .pointerInput(Unit) {
                detectTapGestures { offset ->
                    val canvasSize = size.toSize()
                    val center = Offset(canvasSize.width / 2, canvasSize.height / 2)
                    val dx = offset.x - center.x
                    val dy = offset.y - center.y

                    val angle = (Math.toDegrees(atan2(dy.toDouble(), dx.toDouble())) + 360) % 360

                    val shiftedAngle = (angle + 90) % 360

                    var cumulativeAngle = 0f
                    for (index in sweepAngles.indices) {
                        val msgSweep = sweepAngles[index]
                        if (shiftedAngle >= cumulativeAngle && shiftedAngle < cumulativeAngle + msgSweep) {
                            onSliceClick(keys[index])
                            return@detectTapGestures
                        }
                        cumulativeAngle += msgSweep
                    }
                }
            }
    ) {
        var startAngle = -90f
        data.values.forEachIndexed { index, value ->
            val sweepAngle = 360f * value / totalSum
            drawArc(
                color = colors.getOrElse(index) { Color.Gray },
                startAngle = startAngle,
                sweepAngle = sweepAngle,
                useCenter = true,
                size = size
            )
            startAngle += sweepAngle
        }
    }
}