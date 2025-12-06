package com.piyushmakwana.bmu

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import com.piyushmakwana.bmu.navigation.AppNavigation
import com.piyushmakwana.bmu.ui.common.ConnectivityGlobalSnackBar
import com.piyushmakwana.bmu.ui.theme.BMUTheme
import com.piyushmakwana.bmu.util.connectivity.ConnectivityObserver
import dagger.hilt.android.AndroidEntryPoint
import javax.inject.Inject

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    @Inject lateinit var connectivityObserver: ConnectivityObserver

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            BMUTheme {
                val status by
                connectivityObserver
                    .observe()
                    .collectAsState(initial = ConnectivityObserver.Status.Available)
                val isConnected = status == ConnectivityObserver.Status.Available

                Box(modifier = Modifier.fillMaxSize()) {
                    AppNavigation()
                    ConnectivityGlobalSnackBar(
                        isConnected = isConnected,
                        modifier = Modifier.align(Alignment.BottomCenter)
                    )
                }
            }
        }
    }
}