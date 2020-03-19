package test_demo.test

object jmap_demo {
  def main(args: Array[String]): Unit = {
    println("1...............")
    Thread.sleep(30000)
    var array = new Array[Byte](1024*1024*1000)
    println("2...............")
    Thread.sleep(30000)
//    array = null
//    System.gc()
    println("3...............")
    Thread.sleep(300000L)
  }

}
