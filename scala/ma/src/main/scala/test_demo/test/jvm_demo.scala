package test_demo.test

import java.util.Random

object jvm_demo {
  def main(args: Array[String]): Unit = {
//    println(Runtime.getRuntime.availableProcessors())
//    // 物理内存的1/4
//    val maxMemory: Long = Runtime.getRuntime.maxMemory()
//    // 物理内存的1/64
//    val totalMemory: Long = Runtime.getRuntime.totalMemory()
//
//    println("-Xmx:MAX_MEMORY = " + maxMemory + "(字节)" +(maxMemory/1024/1024) + "MB")
//    println("-Xms:TOTAL_MEMORY = " + totalMemory + "(字节)" +(totalMemory/1024/1024) + "MB")

    var str = "www.bonc.com"
    while (true){
      str = str + new Random().nextInt(888888888) + new Random().nextInt(99999999)
    }
  }
}
