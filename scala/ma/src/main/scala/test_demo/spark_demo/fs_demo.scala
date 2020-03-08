package test_demo.spark_demo

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}

object fs_demo {
  def main(args: Array[String]): Unit = {
    var shutdownMarker = "/tmp/spark-test/stop-spark/aaa"
    var stopFlag = false
    //开始检查hdfs是否有stop-spark文件夹
    val fs = FileSystem.get(new Configuration())
    //如果有返回true，如果没有返回false
    val path = new Path(shutdownMarker)
    stopFlag = fs.exists(path)
    println(stopFlag)
    fs.delete(path,true)

  }

}
