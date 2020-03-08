package test_demo.myextends

object AbstractDetail01 {
  def main(args: Array[String]): Unit = {
    val animal = new Animal03 {
      override def sayHello(): Unit = {
        println("say hello")
      }

      override var food: String = _
    }
    animal.sayHello()
  }
}

abstract class Animal02{
  def sayHi(): Unit ={
    println("sayHi")
  }
}
abstract class Animal03{
  def sayHello()
  var food: String
}

class Dog extends Animal03{
  override def sayHello(): Unit = {

  }

  override var food: String = _
}
