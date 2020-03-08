package test_demo.myextends

object TypeConvert {
  def main(args: Array[String]): Unit = {
    // classof的使用，可以得到类名
    println(classOf[String])
    val s = "king"
    println(s.getClass.getName)  //  使用反射机制

    // isInstanceOf asInstanceOf
    var p1 = new Person200
    var emp = new Emp200

    // 子类转成父类
    p1 = emp
    var emp2: Emp200 = p1.asInstanceOf[Emp200]
    emp2.sayHello()
  }
}

//Person类
class Person200 {
  var name: String = "tom"

  def printName() { //输出名字
    println("Person printName() " + name)
  }

  def sayHi(): Unit = {
    println("sayHi...")
  }
}

//这里我们继承Person
class Emp200 extends Person200 {
  //这里需要显式的使用override
  override def printName() {
    println("Emp printName() " + name)
    //在子类中需要去调用父类的方法,使用super
    super.printName()
    sayHi()
  }

  def sayHello(): Unit = {
    println("sayHello...")
  }
}

