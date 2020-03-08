package test_demo.accompany

object AccompanyObject {
  def main(args: Array[String]): Unit = {
    println(ScalaPerson.sex)
    ScalaPerson.sayHi()
  }
}

class ScalaPerson{
  var name: String = _
}

object ScalaPerson{
  var sex: Boolean = true
  def sayHi(): Unit ={
    println("sayHi")
  }
}