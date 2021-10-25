package com.example.drugrecommendationchatbot

import org.json.JSONException
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.lang.StringBuilder
import java.net.URL
import javax.net.ssl.HttpsURLConnection

object jsonCommunication {
    //singleton 으로 만들었는데, 나중에 동기화문제랑 스레드로 여러개 처리하려면 디자인을 조금 바꿔야할지도...

    val serverUrl = URL("127.0.0.1")

    lateinit var connection :HttpsURLConnection


    private fun sendMessage(keys : MutableList<String>, values:MutableList<String>){
        connection = serverUrl.openConnection() as HttpsURLConnection

        connection.readTimeout = 3000
        connection.connectTimeout = 3000
        connection.doInput = true
        connection.doInput = true
        connection.requestMethod = "PUT"
        connection.useCaches = false
        connection.connect()

        val jsonObject = JSONObject()

        try{
            for(idx in keys.indices){
                jsonObject.put(keys[idx], values[idx])
            }
        }catch (e : JSONException){
            e.printStackTrace()
        }
        connection.disconnect()
    }

    private fun readMessage() : String{
        connection = serverUrl.openConnection() as HttpsURLConnection

        connection.readTimeout = 3000
        connection.connectTimeout = 3000
        connection.doInput = true
        connection.doInput = true
        connection.requestMethod = "GET"
        connection.useCaches = false
        connection.connect()

        val jsonObject = JSONObject()

        val inputStreamReader = InputStreamReader(connection.inputStream, "UTF-8")
        val br = BufferedReader(inputStreamReader)
        val stringBuilder = StringBuilder()
        var line = ""

        do{
            var line = br.readLine()
            if(line == null){
                break
            }
            else{
                stringBuilder.append(line)
            }
        }while(true)

        br.close()
        connection.disconnect()

        return stringBuilder.toString().trim()
    }

}