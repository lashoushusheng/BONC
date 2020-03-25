package test_demo.design_mode.singleton

object TestSingleTon {
  def main(args: Array[String]): Unit = {
    val instance1: Unit = SingleTon.getInstance()
    val instance2: Unit = SingleTon.getInstance()
    if (instance1 == instance2){
      println("=====")
    }

  }
}

class SingleTon private(){}

object SingleTon{
  private var s:SingleTon = null

  def getInstance() = {
    if (s == null){
      s = new SingleTon
    }
    s
  }
}