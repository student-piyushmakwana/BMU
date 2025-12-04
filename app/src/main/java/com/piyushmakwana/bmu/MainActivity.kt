package com.piyushmakwana.bmu

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.piyushmakwana.bmu.navigation.AppNavigation
import com.piyushmakwana.bmu.ui.theme.BMUTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            BMUTheme {
                AppNavigation()
            }
        }
    }
}