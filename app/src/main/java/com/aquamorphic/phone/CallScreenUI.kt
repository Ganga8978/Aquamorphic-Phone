package com.aquamorphic.phone

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun IOS4CallScreen(callerName: String, onAnswer: () -> Unit, onDecline: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xCC1A1A1A))
    ) {
        Button(
            onClick = onDecline,
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF333333)),
            shape = CircleShape,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(top = 40.dp, end = 20.dp)
                .size(40.dp)
        ) {
            Text("X", color = Color.Gray, fontSize = 12.sp)
        }

        Column(
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(top = 100.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = callerName,
                color = Color.White,
                fontSize = 32.sp,
                fontWeight = FontWeight.Light
            )
            Text(
                text = "mobile",
                color = Color.LightGray,
                fontSize = 16.sp,
                modifier = Modifier.padding(top = 8.dp)
            )
        }

        Box(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 60.dp, start = 30.dp, end = 30.dp)
                .fillMaxWidth()
                .height(75.dp)
                .background(Color(0x80000000), shape = RoundedCornerShape(35.dp)),
            contentAlignment = Alignment.CenterStart
        ) {
            Text(
                text = "slide to answer",
                color = Color(0xFF888888),
                modifier = Modifier.align(Alignment.Center),
                fontSize = 20.sp
            )
            
            Button(
                onClick = onAnswer,
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CD964)),
                shape = CircleShape,
                modifier = Modifier
                    .padding(5.dp)
                    .fillMaxHeight()
                    .aspectRatio(1f)
            ) {}
        }
    }
}
