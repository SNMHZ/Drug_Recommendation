package com.example.drugrecommendationchatbot

import java.util.*

data class HTTP_GET_Data_Model(
    var errorMsg : String? = null,
)

data class PostChatMsgModel(
    var date : String? = null,
    var type : String? = null,
    var body : String? = null,
    var seq : Int = 1,
    var no_symptoms : LinkedList<String> = LinkedList<String>(),
    var yes_symptoms : LinkedList<String> = LinkedList<String>()
)

data class GetTest1Model(
    var param : String? = null
)


data class PostResult(
    var result:String? = null
)
