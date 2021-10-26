package com.example.drugrecommendationchatbot

import android.content.Context
import android.hardware.input.InputManager
import android.os.Build
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.inputmethod.InputMethodManager
import android.widget.EditText
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


class ChatFragment : Fragment() {
    lateinit var messageEditText : EditText
    lateinit var sendBtn : AppCompatButton

    lateinit var messageRecyclerViewAdapter : MessageAdapter
    lateinit var messageDataList : MutableList<MessageData>

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
                message_recycler_container.scrollToPosition(messageRecyclerViewAdapter.itemCount - 1)

                //retrofit2 api를 이용해서, json 전송 시작
                var jsonData = PostChatMsgModel("1999-09-09", "0", text)
                retrofitAPI.postChatMsg(jsonData).enqueue(object : Callback<PostResult>{
                    override fun onFailure(call: Call<PostResult>, t: Throwable) {
                        t.printStackTrace()
                        println("fail to response when post the data.")
                    }

                    override fun onResponse(
                        call: Call<PostResult>,
                        response: Response<PostResult>
                    ) {

                        makeChatResponse()
                        println("success to post!")
                    }

                })
            }
        }
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
                messageDataList.add(MessageData(1, jsonObj["param"].toString(), 1, true))
                messageRecyclerViewAdapter.notifyDataSetChanged()
                println("대화내용은 ${response.body()!!["param"]}")
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