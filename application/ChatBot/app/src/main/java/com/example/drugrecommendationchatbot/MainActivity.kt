package com.example.drugrecommendationchatbot

import android.Manifest
import android.content.DialogInterface
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import kotlinx.android.synthetic.main.chat_layout.*
import kotlinx.android.synthetic.main.chat_layout.message_recycler_container
import kotlinx.android.synthetic.main.main_layout.*
import java.security.Permission

class MainActivity : AppCompatActivity() {
    private val REQUEST_CODE = 0
    private val requiredPermissionList = arrayOf(
        Manifest.permission.INTERNET,
        Manifest.permission.ACCESS_COARSE_LOCATION,
        Manifest.permission.READ_EXTERNAL_STORAGE,
        Manifest.permission.WRITE_EXTERNAL_STORAGE
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.main_layout)

        val rejectedPermissionList = permissionCheck()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && rejectedPermissionList.size > 0) {
            requestPermission(rejectedPermissionList)
        }//여기서 권한이 실행되어야만 앱을 진짜 구동하게 하려면, permission획득이 다 되었을때만 fragment나 별도의
        //activity를 시작하도록 변경
    }

    override fun onResume() {
        super.onResume()

        val rejectedPermissionList = permissionCheck()
        if(rejectedPermissionList.size == 0){
            startApp()
        }

    }

    private fun startApp(){
        val fragmentManager = supportFragmentManager
        fragmentManager.beginTransaction().replace(R.id.fragment_frame, ChatFragment()).commit()
        println("채팅화면넘김")


    }

    private fun permissionCheck(): ArrayList<String> {

        val rejectedPermissionList = ArrayList<String>()

        for (permission in requiredPermissionList) {
            if (ContextCompat.checkSelfPermission(
                    this,
                    permission
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                rejectedPermissionList.add(permission)
            }
        }

        return rejectedPermissionList
    }

    private fun requestPermission(requiredPermissionList: ArrayList<String>) {
        val rejectedList = requiredPermissionList.toTypedArray()
        ActivityCompat.requestPermissions(this, rejectedList, REQUEST_CODE)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        when (requestCode) {
            REQUEST_CODE -> {
                if(grantResults.size > 0){
                    requestDeniedPermission()
                }
            }
        }
    }

    private fun requestDeniedPermission(){
        val localBuilder = AlertDialog.Builder(this)

        localBuilder.setTitle("권한 설정")
        localBuilder.setMessage("앱을 구동하기 위해서는 권한이 필요합니다.")
        localBuilder.setPositiveButton("권한 설정", object : DialogInterface.OnClickListener{
            override fun onClick(p0: DialogInterface?, p1: Int) {
                val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).setData(
                    Uri.parse("package:$packageName")
                )
                startActivity(intent)
            }
        })
        localBuilder.setNegativeButton("취소", object:DialogInterface.OnClickListener{
            override fun onClick(p0: DialogInterface?, p1: Int) {
                Toast.makeText(applicationContext,"앱을 종료합니다.", Toast.LENGTH_SHORT).show()
            }
        })
        localBuilder.create().show()

    }


}