package com.example.drugrecommendationchatbot

data class ResponseMessageData (
    val seq : Int,
    val isClear : Boolean,
    val predicts : String,
    val symptoms : String,
    val drugs : String
    )