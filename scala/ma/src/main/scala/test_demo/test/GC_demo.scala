package test_demo.test

class RefCountGC{
  val bigSize = new Array[Int](2*1024*1024)
  var instance:RefCountGC = null
}

object GC_demo {
  def main(args: Array[String]): Unit = {
    var objectA = new RefCountGC
    var objectB = new RefCountGC

    objectA.instance = objectB
    objectB.instance = objectA
    objectA = null
    objectB = null
    System.gc()
  }
}
