package test_demo.mytrait

object traitDemo03 {
  def main(args: Array[String]): Unit = {
    val sheep = new Sheep
    sheep.sayHi()
    sheep.sayHello()
  }
}

trait Trait03{
  def sayHi()

  def sayHello(): Unit ={
    println("say hello~~")
  }
}

class Sheep extends Trait03{
  override def sayHi(): Unit = {
    println("sheep say hi~~")
  }
}