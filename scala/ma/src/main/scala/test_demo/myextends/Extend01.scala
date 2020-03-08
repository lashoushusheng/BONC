package test_demo.myextends

object Extend01 {
  def main(args: Array[String]): Unit = {

  }
}

class Person{
  var name:String = _
  var age:Int = _
  def showInfo(): Unit ={
    println("name: " + this.name)
  }
}

class Student extends Person {
  def studying(): Unit ={
    println(this.name + "starting scala......")
  }
}
