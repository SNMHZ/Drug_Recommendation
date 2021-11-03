package com.example.drugrecommendationchatbot

data class RequestMessageData (
    val seq : Int,
    val systemInfo : String,
    val msg : String,
    val rating : Int
    )