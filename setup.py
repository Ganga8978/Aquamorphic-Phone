import os

folders = [
    ".github/workflows",
    "app/src/main/java/com/aquamorphic/phone"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

files = {
    "gradle.properties": """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""",
    ".github/workflows/build.yml": """name: Build Android APK

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'

    - name: Setup Gradle
      uses: gradle/actions/setup-gradle@v3
      with:
        gradle-version: '8.4'

    - name: Build Debug APK
      run: gradle assembleDebug --stacktrace

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: Aquamorphic-Phone-APK
        path: app/build/outputs/apk/debug/app-debug.apk
""",
    "settings.gradle.kts": """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "Aquamorphic-Phone"
include(":app")
""",
    "build.gradle.kts": """plugins {
    id("com.android.application") version "8.2.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.22" apply false
}
""",
    "app/build.gradle.kts": """plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.aquamorphic.phone"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.aquamorphic.phone"
        minSdk = 28
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.8"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation("androidx.compose.ui:ui:1.6.0")
    implementation("androidx.compose.material3:material3:1.2.0")
}
""",
    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.MANAGE_OWN_CALLS"/>
    <uses-permission android:name="android.permission.READ_PHONE_STATE"/>
    <uses-permission android:name="android.permission.CALL_PHONE"/>
    
    <application
        android:allowBackup="false"
        android:icon="@android:drawable/sym_action_call"
        android:label="Nexus Phone"
        android:theme="@android:style/Theme.DeviceDefault.NoActionBar"
        android:directBootAware="true">
        
        <service
            android:name=".NexusInCallService"
            android:permission="android.permission.BIND_INCALL_SERVICE"
            android:directBootAware="true"
            android:exported="true">
            <meta-data
                android:name="android.telecom.IN_CALL_SERVICE_UI"
                android:value="true" />
            <intent-filter>
                <action android:name="android.telecom.InCallService" />
            </intent-filter>
        </service>

        <activity
            android:name=".CallScreenActivity"
            android:exported="true"
            android:directBootAware="true"
            android:showWhenLocked="true"
            android:turnScreenOn="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.DIAL" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:scheme="tel" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <action android:name="android.intent.action.DIAL" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="tel" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""",
    "app/src/main/java/com/aquamorphic/phone/CallScreenUI.kt": """package com.aquamorphic.phone

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
""",
    "app/src/main/java/com/aquamorphic/phone/NexusInCallService.kt": """package com.aquamorphic.phone

import android.app.role.RoleManager
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.telecom.Call
import android.telecom.InCallService
import android.telecom.VideoProfile
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent

object ActiveCallHolder {
    var currentCall: Call? = null
}

class NexusInCallService : InCallService() {
    override fun onCallAdded(call: Call) {
        super.onCallAdded(call)
        ActiveCallHolder.currentCall = call
        val intent = Intent(this, CallScreenActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        startActivity(intent)
    }

    override fun onCallRemoved(call: Call) {
        super.onCallRemoved(call)
        if (ActiveCallHolder.currentCall == call) {
            ActiveCallHolder.currentCall = null
        }
    }
}

class CallScreenActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestDefaultDialerRole()

        val call = ActiveCallHolder.currentCall
        val callerNumber = call?.details?.handle?.schemeSpecificPart ?: "Preview Call"

        setContent {
            IOS4CallScreen(
                callerName = callerNumber,
                onAnswer = {
                    call?.answer(VideoProfile.STATE_AUDIO_ONLY)
                },
                onDecline = {
                    call?.disconnect()
                    finish()
                }
            )
        }
    }

    private fun requestDefaultDialerRole() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val roleManager = getSystemService(RoleManager::class.java)
            if (roleManager != null && roleManager.isRoleAvailable(RoleManager.ROLE_DIALER) && !roleManager.isRoleHeld(RoleManager.ROLE_DIALER)) {
                val intent = roleManager.createRequestRoleIntent(RoleManager.ROLE_DIALER)
                startActivityForResult(intent, 1001)
            }
        }
    }
}
"""
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("SUCCESS: Real Android compiler files updated!")