package com.bitanswer.authorization

import rtcompute.DStruct.GlobalParams
import com.bitanswer.library.BitAnswer
import com.bitanswer.authorization.JavaAuthentication

object Authentication {
    val SERIAL_NUMBER: String = GlobalParams.serial_number
    if (SERIAL_NUMBER.length != 16){
      println("get SERIAL_NUMBER failure!")
      sys.exit(1)
    }

    def login(): Unit ={
      val Auth = new JavaAuthentication()
      Auth.login(SERIAL_NUMBER)
    }

//    def login(): Unit ={
//      val bitAnswer = new BitAnswer()
//      import bitAnswer.BitAnswerException
//      var bLogin = false
//
//      try {
//        println("In the license certificate.......")
//        // login
//        bitAnswer.login(null, SERIAL_NUMBER, BitAnswer.LoginMode.AUTO)
//        bLogin = true
//        println("Login success.")
//
//      }catch {
//        case ex:BitAnswerException =>
//          println("error code:" + ex.getErrorCode)
//          ex.printStackTrace()
//          println("License certificate failure!")
//          sys.exit(1)
//
//        case ex: Throwable =>
//          ex.printStackTrace()
//      }
//      // Logout
//      try {
//        if(bLogin){
//          bitAnswer.logout()
//          println("Logout success.")
//          println("License has been certified successfully.")
//        }
//
//      }catch {
//        case ex:BitAnswerException =>
//          println(ex.getErrorCode)
//          sys.exit(1)
//      }
//    }

  def main(args: Array[String]): Unit = {
    Authentication.login()
  }
}
