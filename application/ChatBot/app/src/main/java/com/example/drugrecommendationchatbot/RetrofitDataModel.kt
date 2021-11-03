package com.example.drugrecommendationchatbot

data class HTTP_GET_Data_Model(
    var errorMsg : String? = null,
)

data class PostChatMsgModel(
    var date : String? = null,
    var type : String? = null,
    var body : String? = null
)

data class GetTest1Model(
    var param : String? = null
)


data class PostResult(
    var result:String? = null
)
