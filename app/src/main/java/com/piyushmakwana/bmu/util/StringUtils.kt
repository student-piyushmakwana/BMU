package com.piyushmakwana.bmu.util

fun formatPhoneNumber(phone: String): String {
    val cleaned = phone.replace("+91", "").replace(" ", "")
    return if (cleaned.length == 10) {
        "${cleaned.take(5)} ${cleaned.substring(5)}"
    } else {
        cleaned
    }
}
