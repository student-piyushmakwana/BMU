package com.piyushmakwana.bmu.navigation

sealed class Screen(val route: String) {
    data object Splash : Screen("splash_screen")
    data object PublicInfo : Screen("public_info_screen")
}