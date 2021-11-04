package com.example.drugrecommendationchatbot

/**
 * 증상 리스트에서 각 버튼에 대한 이벤트 listener
 *
 * 버튼을 클릭하면, json 전송과 사용자 화면에 전송 메시지 표시를
 * 수행해야 되는데, 이러려면 chatFragment에 접근해야함.(adapter 갱신등)
 */
interface CallbackListener {
    fun sendMsgCallBack(msg : String){}
}