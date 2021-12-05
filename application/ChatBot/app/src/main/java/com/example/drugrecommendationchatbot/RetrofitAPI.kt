package com.example.drugrecommendationchatbot

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.JsonObject
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*

interface RetrofitAPI {
    @POST("/AndroidChatMessage")
    @Headers("accept: application/json",
        "content-type: application/json",
    "Connection: close")
    fun postChatMsg(
        @Body jsonparams: PostChatMsgModel
    ):Call<JsonObject>

    @POST("/AndroidChatMessage")
    @Headers("accept: application/json",
        "content-type: application/json",
        "Connection: close")
    fun postYesOrNoChatMsg(
        @Body jsonparams: PostChatYesOrNoMsgModel
    ):Call<JsonObject>

    //server로부터 응답(결과 get)
    @GET("/GetTest1")
    @Headers("accept: application/json",
        "content-type: application/json",
    "Connection: close")
    fun getTest1():Call<JsonObject>
    //GET 이 맞지 않나?
    //어떤 resource(여기서는 챗봇 메시지 내용)에 대한 result data를 요구하닌까?

    companion object{
        fun setRetrofit() : RetrofitAPI{
            val gson : Gson = GsonBuilder().setLenient().create()

            return Retrofit
                .Builder()
                .baseUrl(StaticVariables.SERVER_URL)
                .addConverterFactory(GsonConverterFactory.create(gson))
                .build()
                .create(RetrofitAPI::class.java)
        }
    }

}