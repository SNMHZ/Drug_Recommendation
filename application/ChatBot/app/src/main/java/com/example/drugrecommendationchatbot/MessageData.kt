package com.example.drugrecommendationchatbot

/**
 * date : 메시지를 작성한 날짜
 * body : 메시지 내용
 * type : 송/수신자 구분(0 : 송신 메시지, 1 : 수신 메시지)
 * correctSendFlag : 해당 메시지의 송/수신 정상 여부
 */

data class MessageData (
    var date : Int,
    var body : String,
    var type : Int,
    var correctSendFlag : Boolean,
    val predicts : ArrayList<Pair<String, Float>> = ArrayList(),
    val drugs : ArrayList<String> = ArrayList())