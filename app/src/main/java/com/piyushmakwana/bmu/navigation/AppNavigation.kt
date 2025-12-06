package com.piyushmakwana.bmu.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.piyushmakwana.bmu.ui.screens.department_detail.DepartmentDetailScreen
import com.piyushmakwana.bmu.ui.screens.public_info.PublicInfoScreen
import com.piyushmakwana.bmu.ui.screens.splash.SplashScreen

@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = Screen.Splash.route) {
        composable(route = Screen.Splash.route) { SplashScreen(navController = navController) }

        composable(
                route = Screen.PublicInfo.route,
                exitTransition = {
                    slideOutOfContainer(
                            towards =
                                    androidx.compose.animation.AnimatedContentTransitionScope
                                            .SlideDirection.Left,
                            animationSpec = androidx.compose.animation.core.tween(500)
                    )
                },
                popEnterTransition = {
                    slideIntoContainer(
                            towards =
                                    androidx.compose.animation.AnimatedContentTransitionScope
                                            .SlideDirection.Right,
                            animationSpec = androidx.compose.animation.core.tween(500)
                    )
                }
        ) { PublicInfoScreen(navController = navController) }

        composable(
                route = Screen.DepartmentDetail.route,
                arguments =
                        listOf(
                                navArgument("bmuId") { type = NavType.StringType },
                                navArgument("shortName") { type = NavType.StringType }
                        ),
                enterTransition = {
                    slideIntoContainer(
                            towards =
                                    androidx.compose.animation.AnimatedContentTransitionScope
                                            .SlideDirection.Left,
                            animationSpec = androidx.compose.animation.core.tween(500)
                    )
                },
                exitTransition = {
                    slideOutOfContainer(
                            towards =
                                    androidx.compose.animation.AnimatedContentTransitionScope
                                            .SlideDirection.Right,
                            animationSpec = androidx.compose.animation.core.tween(500)
                    )
                },
                popEnterTransition = {
                    slideIntoContainer(
                            towards =
                                    androidx.compose.animation.AnimatedContentTransitionScope
                                            .SlideDirection.Right,
                            animationSpec = androidx.compose.animation.core.tween(500)
                    )
                },
                popExitTransition = {
                    slideOutOfContainer(
                            towards =
                                    androidx.compose.animation.AnimatedContentTransitionScope
                                            .SlideDirection.Right,
                            animationSpec = androidx.compose.animation.core.tween(500)
                    )
                }
        ) { DepartmentDetailScreen(navController = navController) }
    }
}
