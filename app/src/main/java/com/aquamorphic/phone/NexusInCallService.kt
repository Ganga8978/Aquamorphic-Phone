package com.aquamorphic.phone

import android.content.Intent
import android.os.Bundle
import android.telecom.Call
import android.telecom.InCallService
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent

class NexusInCallService : InCallService() {
    override fun onCallAdded(call: Call) {
        super.onCallAdded(call)
        val intent = Intent(this, CallScreenActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        startActivity(intent)
    }
}

class CallScreenActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            IOS4CallScreen(
                callerName = "Incoming Call",
                onAnswer = {},
                onDecline = { finish() }
            )
        }
    }
}
