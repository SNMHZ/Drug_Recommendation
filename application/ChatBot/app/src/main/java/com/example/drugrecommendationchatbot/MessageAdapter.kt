package com.example.drugrecommendationchatbot

import android.app.ActionBar
import android.content.Context
import android.content.DialogInterface
import android.graphics.Color
import android.graphics.Typeface
import android.hardware.camera2.CameraDevice
import android.text.Layout
import android.text.Spannable
import android.text.SpannableString
import android.text.style.RelativeSizeSpan
import android.text.style.StyleSpan
import android.util.AttributeSet
import android.util.DisplayMetrics
import android.util.LayoutDirection
import android.util.TypedValue
import android.view.Gravity
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.appcompat.widget.AppCompatButton
import androidx.core.view.children
import androidx.core.view.marginLeft
import androidx.recyclerview.widget.RecyclerView
import com.github.mikephil.charting.animation.Easing
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.charts.PieChart
import com.github.mikephil.charting.components.Description
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.PieData
import com.github.mikephil.charting.data.PieDataSet
import com.google.gson.JsonObject
import kotlinx.android.synthetic.main.chat_layout.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.security.KeyStore
import com.github.mikephil.charting.utils.ColorTemplate

import com.github.mikephil.charting.data.PieEntry
import com.github.mikephil.charting.utils.MPPointF

class MessageAdapter(private val context : Context, private val chatFragment : ChatFragment) : RecyclerView.Adapter<RecyclerView.ViewHolder>(){

    var messageDataList = mutableListOf<MessageData>()
    lateinit var selectSymptomBtnListener : CallbackListener
    var currentCount = 0

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        if(viewType == StaticVariables.LEFT_CHAT){

            return LeftViewHolder(LayoutInflater.from(context).inflate(R.layout.message_recycler_item_left
                ,parent, false))

        }
        else if(viewType == StaticVariables.RIGHT_CHAT){

            return RightViewHolder(LayoutInflater.from(context).inflate(R.layout.message_recycler_item_right
                ,parent, false))

        }else if(viewType == StaticVariables.RECEIVE_MSG_LOADING){

            println("로딩 메시지 출력 viewholder 생성")
            return LeftLoadingViewHolder(LayoutInflater.from(context).inflate(R.layout.message_loading_item_left
                ,parent, false))


        }else if(viewType == StaticVariables.SYSTEM_MSG){
            return SystemMessageViewHolder(LayoutInflater.from(context).inflate(R.layout.message_system_log_item
                ,parent, false))

        }else if(viewType == StaticVariables.RECEIVE_YES_OR_NO_MSG){
            return LeftYesOrNoSelectionViewHolder(LayoutInflater.from(context).inflate(R.layout.message_recycler_itme_left_yes_or_no_selection,
                parent, false))

        }
        else{
            return LeftSelectionViewHolder(LayoutInflater.from(context).inflate(R.layout.selection_symptom_veiw_layout
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
            //loading은 딱히 bind 필요 없을거 같음

            StaticVariables.SYSTEM_MSG->{
                (holder as SystemMessageViewHolder).bind(messageDataList[position])
            }
            StaticVariables.RECEIVE_YES_OR_NO_MSG->{
                (holder as LeftYesOrNoSelectionViewHolder).bind(messageDataList[position])
            }
        }
    }

    override fun getItemViewType(position: Int): Int {
        return messageDataList[position].type
    }

    inner class SystemMessageViewHolder(itemView: View):RecyclerView.ViewHolder(itemView){
        private val messageBody = itemView.findViewById<TextView>(R.id.system_message_body)
        fun bind(data : MessageData){
            messageBody.text = data.body
        }

    }


    inner class LeftViewHolder(itemView : View) : RecyclerView.ViewHolder(itemView){
        private val messageBody  :TextView = itemView.findViewById(R.id.message_body)
        private val pieChart = itemView.findViewById<PieChart>(R.id.circular_chart)

        fun bind(data : MessageData){
            if(data.predicts.size > 0 || data.eof == 0){
                println("일반 leftview 생성!!")
                pieChart.description.isEnabled = false
                pieChart.setExtraOffsets(5f, 10f, 5f, 5f)

                pieChart.isDrawHoleEnabled = false

                pieChart.dragDecelerationFrictionCoef = 0.95f
                pieChart.setEntryLabelColor(Color.BLACK)

                val yValues = ArrayList<PieEntry>()

                var others = 0f
                var sum = 0f
                messageBody.text = data.body.replace("\"", "")

                for(item in data.predicts){
                    yValues.add(PieEntry(item.second.toFloat(), item.first))
                    sum += item.second.toFloat()
                }
                others = 1f - sum
                yValues.add(PieEntry(others, "others"))

                val description = Description()
                description.setText("예상되는 증상") //라벨

                description.setTextSize(15F)
                pieChart.description = description

                pieChart.animateY(1000, Easing.EaseInOutCubic) //애니메이션

                val dataSet = PieDataSet(yValues, "Conditions")
                dataSet.sliceSpace = 3f
                dataSet.selectionShift = 5f
                dataSet.setColors(*ColorTemplate.COLORFUL_COLORS)

                val data = PieData(dataSet)
                data.setValueTextSize(10f)
                data.setValueTextColor(Color.YELLOW)

                pieChart.setData(data)

                pieChart.visibility = View.VISIBLE

            }else{
                messageBody.text = data.body
                pieChart.visibility = View.GONE
            }

            if(data.date != -1){

            }

        }
    }

    inner class RightViewHolder(itemView : View) : RecyclerView.ViewHolder(itemView){
        private val messageBody  :TextView = itemView.findViewById(R.id.message_body)

        fun bind(data : MessageData){
            messageBody.text = data.body
        }

    }

    inner class LeftLoadingViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView){

    }

    inner class LeftYesOrNoSelectionViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView){
        val messageBody = itemView.findViewById<TextView>(R.id.message_body)
        //val yesBtn = itemView.findViewById<com.dd.CircularProgressButton>(R.id.yes_btn)
        val yesBtn = itemView.findViewById<ImageView>(R.id.yes_btn)
        val noBtn = itemView.findViewById<ImageView>(R.id.no_btn)
        //val noBtn = itemView.findViewById<com.dd.CircularProgressButton>(R.id.no_btn)


        fun bind(data : MessageData){

            //yesBtn.progress = 0
            //noBtn.progress = 0

            //아이템들이 새로 그려질 때, 버튼들이 다시 선택되는 현상을 방지
            if(data.alreaySelected){
                println("매번 호출됨?")
                yesBtn.isClickable = false
                noBtn.isClickable = false

                if(data.selected_YesBtn){
                    //yesBtn.progress = 100
                    yesBtn.isSelected = true
                }else{
                    noBtn.isSelected = true
                    //noBtn.progress = -1
                }
            }else{
                yesBtn.isSelected = false
                noBtn.isSelected = false
            }

            messageBody.text = data.body

            //yesBtn.isIndeterminateProgressMode = true
            //noBtn.isIndeterminateProgressMode = true

            yesBtn.setOnClickListener {
                val yesLinkedList = chatFragment.yesSymptomList
                val noLinkedList = chatFragment.noSymptomList

                data.alreaySelected = true
                data.selected_YesBtn = true
                yesBtn.isClickable = false
                noBtn.isClickable = false
                yesBtn.isSelected = true

                //yesBtn.progress = 50

                yesLinkedList.add(data.sym_word)


                var jsonData = PostChatMsgModel("1999-09-09", "0",  StaticVariables.initialSentence, yes_symptoms = yesLinkedList, no_symptoms = noLinkedList, seq = chatFragment.seq, )
                RetrofitAPI.setRetrofit().postChatMsg(jsonData).enqueue(object : Callback<JsonObject> {
                    override fun onFailure(call: Call<JsonObject>, t: Throwable) {
                        t.printStackTrace()
                        println("fail to response when post the data. so recently added last element will be deleted.")
                        yesLinkedList.pop()
                        //yesBtn.progress = 0
                        yesBtn.isClickable = true
                        noBtn.isClickable = true
                    }

                    override fun onResponse(
                        call: Call<JsonObject>,
                        response: Response<JsonObject>
                    ) {
                        print("======call json data logcat=====")
                        println(jsonData)

                        chatFragment.waitingPostMsg()

                        CoroutineScope(Dispatchers.Main).launch{
                            //loadingResponseMessage()
                            delay(3000)
                            //makeChatResponse()
                            messageDataList[messageDataList.size - 1] = chatFragment.addReceivedPostMsg(response.body()!!)
                            chatFragment.messageRecyclerViewAdapter.notifyItemChanged(messageDataList.size - 1)
                            chatFragment.message_recycler_container.smoothScrollToPosition(messageDataList.size)
                            println("어뎁터안에서 데이터가 바뀌는가?")
                        }
                        println(response.body())
                        println("success to post!")
                        //yesBtn.progress = 100
                    }

                })
            }
            noBtn.setOnClickListener {
                val yesLinkedList = chatFragment.yesSymptomList
                val noLinkedList = chatFragment.noSymptomList

                data.alreaySelected = true
                data.selectedNoBtn = true
                yesBtn.isClickable = false
                noBtn.isClickable = false
                noBtn.isSelected = true

                //noBtn.progress = 50

                noLinkedList.add(data.sym_word)


                var jsonData = PostChatMsgModel( "1999-09-09", "0", StaticVariables.initialSentence, yes_symptoms = yesLinkedList, no_symptoms = noLinkedList, seq = chatFragment.seq, )
                RetrofitAPI.setRetrofit().postChatMsg(jsonData).enqueue(object : Callback<JsonObject> {
                    override fun onFailure(call: Call<JsonObject>, t: Throwable) {
                        t.printStackTrace()
                        println("fail to response when post the data. so recently added last element will be deleted.")
                        noLinkedList.pop()
                        //noBtn.progress = 0
                        yesBtn.isClickable = true
                        noBtn.isClickable = true
                    }

                    override fun onResponse(
                        call: Call<JsonObject>,
                        response: Response<JsonObject>
                    ) {
                        print("======call json data logcat=====")
                        println(jsonData)

                        chatFragment.waitingPostMsg()

                        CoroutineScope(Dispatchers.Main).launch{
                            //loadingResponseMessage()
                            delay(3000)
                            //makeChatResponse()
                            messageDataList[messageDataList.size - 1] = chatFragment.addReceivedPostMsg(response.body()!!)
                            chatFragment.messageRecyclerViewAdapter.notifyItemChanged(messageDataList.size - 1)
                            chatFragment.message_recycler_container.smoothScrollToPosition(messageDataList.size)
                            println("어뎁터안에서 데이터가 바뀌는가?")
                        }
                        println(response.body())
                        println("success to post!")
                        //noBtn.progress = -1
                    }

                })
            }
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
            val titleMessageText = messageBody.text.toString()
            val highlightWordList = arrayOf("해당되는 증상")

            println("현재 차일드 뷰 개수 = ${messageLayout.childCount}")

            messageBody.text = highlightWord(highlightWordList, titleMessageText)

            if(messageLayout.childCount >= 5)return
            //스크롤할때마다, viewholder가 호출되는데
            //이 때, 기존에 생성된 layout객체를 참조해서
            //스클로할때마다 버튼이 계속생성되는 문제가 발생함

            val symptomList = data.body.split(",")
            println("증상 개수 = ${symptomList.size} \n 증상 = $symptomList")
            for(eachSymptom in symptomList){
                val selectionBtn = makeSymptomBtnLayout(eachSymptom)
                selectionBtn.setOnClickListener {
                    var jsonData = PostChatMsgModel("1999-09-09", "0", eachSymptom)
                    RetrofitAPI.setRetrofit().postChatMsg(jsonData).enqueue(object : Callback<JsonObject> {
                        override fun onFailure(call: Call<JsonObject>, t: Throwable) {
                            t.printStackTrace()
                            println("fail to response when post the data.")
                        }

                        override fun onResponse(
                            call: Call<JsonObject>,
                            response: Response<JsonObject>
                        ) {
                            println("buttons disable 하기")
                            selectSymptomBtnListener.sendMsgCallBack(eachSymptom)
                            disableBtns(messageLayout)
                            println("success to post!")
                        }

                    })
                    println("$eachSymptom 버튼 누름!")
                }

                messageLayout.addView(selectionBtn)
            }

        }

    }


    private fun disableBtns(messageLayout:LinearLayout){
        /**
         * 증상 리스트 버튼을 눌러서, 해당 증상을 메시지로 전송하면
         * 모든 버튼들이 disable되어서 다시는 터치 되지 못하게 해야함
         */
        for(childViewIdx in 1 until messageLayout.childCount){
            val btn = messageLayout.getChildAt(childViewIdx) as Button
            btn.isEnabled = false
        }

    }

    private fun highlightWord(targetList : Array<String>, source : String) : SpannableString{
        /**
         * 문장 중에서 1개 이상의 단어에 대해 bold, size 변경을 적용
         */
        val spannableString = SpannableString(source)

        for(word in targetList){
            var start = source.indexOf(word)
            var end = start + word.length

            spannableString.setSpan(StyleSpan(Typeface.BOLD), start, end, Spannable.SPAN_EXCLUSIVE_EXCLUSIVE)
            spannableString.setSpan(RelativeSizeSpan(1.1f), start, end, SpannableString.SPAN_EXCLUSIVE_EXCLUSIVE)
        }

        return spannableString
    }

    private fun makeSymptomBtnLayout(symptom : String) : Button{
        val selectionBtn = Button(context)
        val layoutParams = ActionBar.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        )
        layoutParams.setMargins(60, 10, 60 ,40)
        layoutParams.gravity = Gravity.CENTER
        selectionBtn.text = symptom
        selectionBtn.width = getDPI(100)
        selectionBtn.height = getDPI(200)
        selectionBtn.layoutParams = layoutParams

        selectionBtn.setBackgroundResource(R.drawable.symptom_btn_bg)

        return selectionBtn
    }

    private fun getDPI(dp : Int) : Int{
        return TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, dp.toFloat(), DisplayMetrics()).toInt()
    }






}