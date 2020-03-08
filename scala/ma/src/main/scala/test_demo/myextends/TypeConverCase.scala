package test_demo.myextends

object TypeConverCase {
  def main(args: Array[String]): Unit = {
    val stu = new Stuent400
    val emp = new Emp400
    test(stu)
    test(emp)
  }
  // 写了一个参数多态代码
  // 一个父类的引用可以接收所有子类的引用
  def test(p:Person400): Unit = {
    p match {
      case emp400: Emp400 =>
        p.asInstanceOf[Emp400].ShowInfo()
      case stuent400: Stuent400 =>
        p.asInstanceOf[Stuent400].cry()
      case _ =>
    }
  }
}

class Person400{
  def printName(): Unit ={
    println("Person400 printName")
  }

  def sayOk(): Unit ={
    println("Person400 printName")
  }
}

class Stuent400 extends Person400{
  val stuId = 100
  override def printName(): Unit ={
    println("Stuent400 printName")
  }
  def cry(): Unit ={
    println("Stuent id=" + this.stuId)
  }
}

class Emp400 extends Person400{
  val empId = 100
  override def printName(): Unit ={
    println("Emp400 printName")
  }
  def ShowInfo(): Unit ={
    println("Emp400 id=" + this.empId)
  }
}