package com.aquamorphic.phone

import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.Orientation
import androidx.compose.foundation.gestures.draggable
import androidx.compose.foundation.gestures.rememberDraggableState
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.roundToInt

@Composable
fun IOS4CallScreen(callerName: String, onAnswer: () -> Unit, onDecline: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(Color(0xEE101820), Color(0xEE05080C))
                )
            )
    ) {
        // Tiny, pocket-safe decline button at the top right
        Button(
            onClick = onDecline,
            colors = ButtonDefaults.buttonColors(containerColor = Color(0x66333333)),
            shape = CircleShape,
            contentPadding = PaddingValues(0.dp),
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(top = 48.dp, end = 24.dp)
                .size(36.dp)
        ) {
            Text("✕", color = Color(0xFFAAAAAA), fontSize = 14.sp)
        }

        // Caller Information Header
        Column(
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(top = 110.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = callerName,
                color = Color.White,
                fontSize = 34.sp,
                fontWeight = FontWeight.Light
            )
            Text(
                text = "mobile",
                color = Color(0xFF99AABB),
                fontSize = 17.sp,
                modifier = Modifier.padding(top = 6.dp)
            )
        }

        // Authentic iOS 4 Drag-to-Answer Slider
        BoxWithConstraints(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 64.dp, start = 28.dp, end = 28.dp)
                .fillMaxWidth()
                .height(76.dp)
                .background(Color(0x99000000), shape = RoundedCornerShape(38.dp))
                .padding(6.dp),
            contentAlignment = Alignment.CenterStart
        ) {
            val maxSlidePx = with(LocalDensity.current) { (maxWidth - 64.dp).toPx() }
            var offsetX by remember { mutableStateOf(0f) }

            Text(
                text = "slide to answer",
                color = Color(0xFF8899AA),
                modifier = Modifier.align(Alignment.Center),
                fontSize = 20.sp
            )

            Box(
                modifier = Modifier
                    .offset { IntOffset(offsetX.roundToInt(), 0) }
                    .size(64.dp)
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(Color(0xFF66EE77), Color(0xFF28A745))
                        ),
                        shape = CircleShape
                    )
                    .draggable(
                        orientation = Orientation.Horizontal,
                        state = rememberDraggableState { delta ->
                            offsetX = (offsetX + delta).coerceIn(0f, maxSlidePx)
                        },
                        onDragStopped = {
                            if (offsetX > maxSlidePx * 0.75f) {
                                onAnswer()
                            } else {
                                offsetX = 0f
                            }
                        }
                    ),
                contentAlignment = Alignment.Center
            ) {
                Text("➔", color = Color.White, fontSize = 24.sp)
            }
        }
    }
}
