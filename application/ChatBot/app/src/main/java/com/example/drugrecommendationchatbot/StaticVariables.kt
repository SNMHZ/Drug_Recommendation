package com.example.drugrecommendationchatbot

import java.util.*

object StaticVariables {
    const val LEFT_CHAT = 1
    const val RIGHT_CHAT = 0
    const val SEND_MSG = 0
    const val SYSTEM_MSG = 7
    const val RECEIVE_YES_OR_NO = 10
    const val RECEIVE_MSG_LOADING = 5
    const val RECEIVE_NORMAL_MSG = 1
    const val RECEIVE_SELECTION_MSG = 2
    //모델 예측을 향상시키기 위해, 가능한 symptom 후부중에서 선택하도록 요구하는 메시지

    var SERVER_URL ="http://10.0.2.2:5000"
        //"http://172.20.42.206:5000"
        //"http://10.0.2.2:5000"


    var PIE_CHART_FLAG = false
    var yesSymList = LinkedList<String>()
    var noSymList = LinkedList<String>()
}