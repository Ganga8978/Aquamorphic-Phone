package com.aquamorphic.phone

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
