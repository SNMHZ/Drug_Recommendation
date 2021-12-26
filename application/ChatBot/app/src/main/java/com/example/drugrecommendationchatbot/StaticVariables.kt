package com.example.drugrecommendationchatbot

object StaticVariables {
    const val LEFT_CHAT = 1
    const val RIGHT_CHAT = 0
    const val SEND_MSG = 0
    const val SYSTEM_MSG = 7
    const val RECEIVE_MSG_LOADING = 5
    const val RECEIVE_YES_OR_NO_MSG = 6
    const val RECEIVE_NORMAL_MSG = 1
    const val RECEIVE_SELECTION_MSG = 2
    //모델 예측을 향상시키기 위해, 가능한 symptom 후부중에서 선택하도록 요구하는 메시지

    var SERVER_URL = "http://10.0.2.2:5000"
        // "http://snmhz325.asuscomm.com:5000"
        //"http://10.0.2.2:5000"

    var PIE_CHART_FLAG = false

    var initialSentence : String = ""
}