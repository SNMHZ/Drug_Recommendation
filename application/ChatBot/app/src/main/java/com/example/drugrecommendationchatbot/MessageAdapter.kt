package com.example.drugrecommendationchatbot

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView

class MessageAdapter(private val context : Context) : RecyclerView.Adapter<MessageAdapter.ViewHolder>(){

    var messageDataList = mutableListOf<MessageData>()

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(context).inflate(R.layout.message_recycler_item ,parent, false)
        return ViewHolder(view)
    }

    override fun getItemCount(): Int {
        return messageDataList.size
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(messageDataList[position])
    }

    inner class ViewHolder(itemView : View) : RecyclerView.ViewHolder(itemView){
        private val messageBody : TextView = itemView.findViewById(R.id.message_body)

        fun bind(data : MessageData){
            messageBody.text = data.body
            if(data.type == 0){
                messageBody.background = ContextCompat.getDrawable(context, R.drawable.outgoing_chat_bubble_bg)
            }else{
                messageBody.background = ContextCompat.getDrawable(context, R.drawable.incoming_chat_bubble_bg)
            }
        }
    }


}