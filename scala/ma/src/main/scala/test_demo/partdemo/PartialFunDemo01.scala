package test_demo.partdemo

object PartialFunDemo01 {
  def main(args: Array[String]): Unit = {
    val list = List(1,2,3,4,"hello")
    list.filter(f1)
  }

  def f1(n:Any):Boolean={
    n.isInstanceOf[Int]
  }
}
