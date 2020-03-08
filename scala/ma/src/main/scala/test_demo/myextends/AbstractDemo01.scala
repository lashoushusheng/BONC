package test_demo.myextends

object AbstractDemo01 {
  def main(args: Array[String]): Unit = {

  }
}

abstract class Animal{
  var name: String
  val age: Int
  var color: String = "black"
  def cry()
}

