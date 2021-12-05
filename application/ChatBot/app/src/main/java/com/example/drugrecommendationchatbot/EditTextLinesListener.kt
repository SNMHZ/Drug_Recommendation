package com.example.drugrecommendationchatbot

import android.text.Editable
import android.text.TextWatcher
import android.widget.EditText

class EditTextLinesListener(editText: EditText, maxLines : Int) : TextWatcher {
    var editText : EditText = editText
    var maxLines = maxLines
    var lastValue = ""

    override fun beforeTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {
        lastValue = p0.toString()
    }

    override fun afterTextChanged(p0: Editable?) {
        if (editText.lineCount > maxLines) {
            var selectionStart = editText.selectionStart - 1
            editText.setText(lastValue)
            if (selectionStart >= editText.length()) {
                selectionStart = editText.length()
            }
            editText.setSelection(selectionStart)
        }
    }

    override fun onTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {
    }

}