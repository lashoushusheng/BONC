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

  def main(args: Array[String]): Unit = {
    Authentication.login()
  }
}
