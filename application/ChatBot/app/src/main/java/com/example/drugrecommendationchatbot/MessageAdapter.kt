package com.example.drugrecommendationchatbot

import android.content.Context
import android.content.DialogInterface
import android.util.DisplayMetrics
import android.util.TypedValue
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MessageAdapter(private val context : Context) : RecyclerView.Adapter<RecyclerView.ViewHolder>(){

    var messageDataList = mutableListOf<MessageData>()

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        if(viewType == StaticVariables.LEFT_CHAT){
            return LeftViewHolder(LayoutInflater.from(context).inflate(R.layout.message_recycler_item_left
                ,parent, false))
        }
        else if(viewType == StaticVariables.RIGHT_CHAT){

            return RightViewHolder(LayoutInflater.from(context).inflate(R.layout.message_recycler_item_right
                ,parent, false))
        }else{
            return LeftSelectionViewHolder(LayoutInflater.from(context).
            inflate(R.layout.selection_symptom_veiw_layout
                ,parent, false))
        }

    }

    override fun getItemCount(): Int {
        return messageDataList.size
    }

    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        val type = messageDataList[position].type

        when(type){
            StaticVariables.LEFT_CHAT->{
                (holder as LeftViewHolder).bind(messageDataList[position])
            }
            StaticVariables.RIGHT_CHAT->{
                (holder as RightViewHolder).bind(messageDataList[position])
            }
            StaticVariables.RECEIVE_SELECTION_MSG->{
                (holder as LeftSelectionViewHolder).bind(messageDataList[position])
            }
        }
    }

    override fun getItemViewType(position: Int): Int {
        return messageDataList[position].type
    }


    inner class LeftViewHolder(itemView : View) : RecyclerView.ViewHolder(itemView){
        private val messageBody  :TextView = itemView.findViewById(R.id.message_body)

        fun bind(data : MessageData){
            messageBody.text = data.body
        }
    }

    inner class RightViewHolder(itemView : View) : RecyclerView.ViewHolder(itemView){
        private val messageBody  :TextView = itemView.findViewById(R.id.message_body)

        fun bind(data : MessageData){
            messageBody.text = data.body
        }

    }

    inner class LeftSelectionViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView){
        private val messageBody : TextView = itemView.findViewById(R.id.selection_message_body)
        private val messageLayout : LinearLayout = itemView.findViewById(R.id.symptom_list_layout)

        /**
         * 가능한 한 symptom 들은 문자열 list로 처리
         * sore, sick, anxiety
         * 이런 형태로
         */


        fun bind(data : MessageData){
            //messageLayout.addView()
            messageBody.text = "다음 증상 중 해당되는게 있으신가요?"
            val symptomList = data.body.split(",")
            println("증상 개수 = ${symptomList.size} \n 증상 = $symptomList")
            for(eachSymptom in symptomList){
                val selectionBtn = Button(context)
                selectionBtn.width = getDPI(100)
                selectionBtn.height = getDPI(200)
                selectionBtn.text = eachSymptom
                selectionBtn.setOnClickListener {
                    var jsonData = PostChatMsgModel("1999-09-09", "0", eachSymptom)
                    RetrofitAPI.setRetrofit().postChatMsg(jsonData).enqueue(object : Callback<PostResult> {
                        override fun onFailure(call: Call<PostResult>, t: Throwable) {
                            t.printStackTrace()
                            println("fail to response when post the data.")
                        }

                        override fun onResponse(
                            call: Call<PostResult>,
                            response: Response<PostResult>
                        ) {

                            println("success to post!")
                        }

                    })
                    println("$eachSymptom 버튼 누름!")
                }

                messageLayout.addView(selectionBtn)
            }
        }

    }

    private fun getDPI(dp : Int) : Int{
        return TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, dp.toFloat(), DisplayMetrics()).toInt()
    }






}