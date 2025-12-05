package com.piyushmakwana.bmu.navigation

sealed class Screen(val route: String) {
    data object Splash : Screen("splash_screen")
    data object PublicInfo : Screen("public_info_screen")
    data object DepartmentDetail : Screen("department_detail_screen/{bmuId}") {
        fun createRoute(bmuId: Int) = "department_detail_screen/$bmuId"
    }
}