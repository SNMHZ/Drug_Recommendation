package com.example.drugrecommendationchatbot

import android.content.Context
import android.hardware.input.InputManager
import android.os.Build
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.inputmethod.InputMethodManager
import android.widget.AdapterView
import android.widget.EditText
import android.widget.ImageView
import androidx.appcompat.widget.AppCompatButton
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.gson.JsonObject
import kotlinx.android.synthetic.main.chat_layout.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import kotlin.reflect.typeOf
import com.github.ybq.android.spinkit.*
import kotlinx.coroutines.*
import com.github.mikephil.charting.*


class ChatFragment : Fragment() {
    lateinit var messageEditText : EditText
    lateinit var sendBtn : ImageView

    lateinit var messageRecyclerViewAdapter : MessageAdapter
    lateinit var messageDataList : MutableList<MessageData>

    lateinit var sendSymptomCallBackListener : CallbackListener

    var retrofitAPI = RetrofitAPI.setRetrofit()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        message_recycler_container.adapter = messageRecyclerViewAdapter
        /**
         * adapter를 view가 생성될때 만들고, 실제 layout 요소의 adapter에 붙이는걸
         * onViewCreated()에서 진행해야 함.
         */

        sendInfo()
        initializeViewComponent()

        println(messageRecyclerViewAdapter.itemCount)
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        initializeRecyclerView()
        return inflater.inflate(R.layout.chat_layout, container, false)
    }

    private fun initializeRecyclerView(){
        messageRecyclerViewAdapter = MessageAdapter(requireContext())
        messageDataList = mutableListOf<MessageData>()

        messageDataList.apply {
            add(MessageData(3, "수신용 더미 대화1", 1, true))
            add(MessageData(3, "발신용 더미 대화2", 0, true))
        }
        messageRecyclerViewAdapter.messageDataList = messageDataList
        sendSymptomCallBackListener = object : CallbackListener{
            override fun sendMsgCallBack(msg: String) {
                messageDataList.add(MessageData(1, msg, 0, true))
                messageRecyclerViewAdapter.notifyItemInserted(messageRecyclerViewAdapter.itemCount - 1)
                message_recycler_container.scrollToPosition(messageRecyclerViewAdapter.itemCount - 1)
                CoroutineScope(Dispatchers.Main).launch{
                    loadingResponseMessage()
                    delay(3000)
                    makeChatResponse()
                }
            }
        }
        messageRecyclerViewAdapter.selectSymptomBtnListener = sendSymptomCallBackListener
        messageRecyclerViewAdapter.notifyDataSetChanged()

    }

    private fun initializeViewComponent(){
        sendBtn = requireView().findViewById(R.id.send_btn)
        messageEditText = requireView().findViewById(R.id.message_edit_text)


        sendBtn.setOnClickListener {
            val text = messageEditText.text.toString()
            if(text.isNotBlank()){
                messageDataList.add(MessageData(7, text, 0, true))
                messageEditText.text = null
                messageEditText.clearFocus()
                hideSoftKeyPad(messageEditText)
                messageRecyclerViewAdapter.notifyItemInserted(messageRecyclerViewAdapter.itemCount - 1)
                message_recycler_container.scrollToPosition(messageRecyclerViewAdapter.itemCount - 1)

                waitingPostMsg()
                //post

                //retrofit2 api를 이용해서, json 전송 시작
                var jsonData = PostChatMsgModel("1999-09-09", "0", text)
                retrofitAPI.postChatMsg(jsonData).enqueue(object : Callback<JsonObject>{
                    override fun onFailure(call: Call<JsonObject>, t: Throwable) {
                        t.printStackTrace()
                        println("fail to response when post the data.")
                    }

                    override fun onResponse(
                        call: Call<JsonObject>,
                        response: Response<JsonObject>
                    ) {

                        CoroutineScope(Dispatchers.Main).launch{
                            //loadingResponseMessage()
                            delay(3000)
                            //makeChatResponse()
                            messageDataList[messageDataList.size - 1] = addReceivedPostMsg(response.body()!!)
                            messageRecyclerViewAdapter.notifyItemChanged(messageDataList.size - 1)
                            message_recycler_container.smoothScrollToPosition(messageDataList.size)
                        }
                        println(response.body())
                        println("success to post!")
                    }

                })
            }
        }
    }
    private fun addReceivedPostMsg(data : JsonObject) : MessageData{
        val body = data["body"].toString()

        val result = MessageData(1, body, StaticVariables.RECEIVE_NORMAL_MSG, true)
        if(!data["predicts"].isJsonNull){
            val predicts = data["predicts"] as JsonObject
            println("predicts 확인")
            println(predicts)
            for(i in 0 until 3){
                var eachSymptomJsonObject = predicts[i.toString()] as JsonObject
                println("predicts의 각 item 확인")
                println(eachSymptomJsonObject)
                var condition = eachSymptomJsonObject["condition"].asString
                var prob = eachSymptomJsonObject["prob"].asFloat
                result.predicts.add(Pair(condition, prob))
            }
            println("type 확인")
            println(predicts)
        }

        return result
    }

    private fun waitingPostMsg(){
        messageDataList.add(MessageData(0, "loading", StaticVariables.RECEIVE_MSG_LOADING, true))
        messageRecyclerViewAdapter.notifyItemInserted(messageRecyclerViewAdapter.itemCount)
        message_recycler_container.scrollToPosition(messageRecyclerViewAdapter.itemCount - 1)

    }

    private suspend fun loadingResponseMessage(){
        messageDataList.add(MessageData(0, "t", StaticVariables.RECEIVE_MSG_LOADING, true))
        //messageRecyclerViewAdapter.notifyItemRangeChanged(0, messageRecyclerViewAdapter.itemCount)
        messageRecyclerViewAdapter.notifyItemInserted(messageRecyclerViewAdapter.itemCount)
        message_recycler_container.scrollToPosition(messageRecyclerViewAdapter.itemCount - 1)

    }

    private fun makeChatResponse(){

        retrofitAPI.getTest1().enqueue(object : Callback<JsonObject>{
            override fun onFailure(call: Call<JsonObject>, t: Throwable) {
                println("error 메시지 : ")
                t.printStackTrace()
                println("get 실패")
            }


            override fun onResponse(call: Call<JsonObject>, response: Response<JsonObject>) {
                var jsonObj = response.body()!!
                val type = jsonObj["type"].toString()
                println("type 출력 = $type")
                if(type == "\"result_msg\""){
                    val newData = MessageData(1, jsonObj["body"].toString().replace("\"", ""), StaticVariables.RECEIVE_NORMAL_MSG, true)
                    messageDataList[messageRecyclerViewAdapter.itemCount - 1] = newData
                }
                else if(type == "\"selection_msg\""){
                    val newData = MessageData(1, jsonObj["body"].toString().replace("\"", ""), StaticVariables.RECEIVE_SELECTION_MSG, true)
                    messageDataList[messageRecyclerViewAdapter.itemCount - 1] = newData
                }
                messageRecyclerViewAdapter.notifyItemChanged(messageRecyclerViewAdapter.itemCount - 1)
                message_recycler_container.scrollToPosition(messageRecyclerViewAdapter.itemCount - 1)

                println("대화내용은 ${response.body()!!["body"]}")
            }

        })
    }

    private fun hideSoftKeyPad(editText : EditText){
        val inputManager = requireActivity().getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
        inputManager.hideSoftInputFromWindow(editText.windowToken, 0)
    }

    private fun sendInfo(){
        val model = Build.MODEL
        val osVersion = Build.VERSION.RELEASE.toString()
        val manufacturer = Build.MANUFACTURER

        messageDataList.add(MessageData(0, "model = $model\nos = $osVersion\n" +
                "제조사 = $manufacturer\n", 0, true) )
    }



}