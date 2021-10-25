package com.example.drugrecommendationchatbot

import android.content.Context
import android.hardware.input.InputManager
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
import kotlinx.android.synthetic.main.chat_layout.*


class ChatFragment : Fragment() {
    lateinit var messageEditText : EditText
    lateinit var sendBtn : AppCompatButton

    lateinit var messageRecyclerViewAdapter : MessageAdapter
    lateinit var messageDataList : MutableList<MessageData>


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        message_recycler_container.adapter = messageRecyclerViewAdapter
        /**
         * adapter를 view가 생성될때 만들고, 실제 layout 요소의 adapter에 붙이는걸
         * onViewCreated()에서 진행해야 함.
         */

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
            }
        }
    }

    private fun hideSoftKeyPad(editText : EditText){
        val inputManager = requireActivity().getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
        inputManager.hideSoftInputFromWindow(editText.windowToken, 0)
    }



}