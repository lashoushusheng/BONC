package test_demo.spark_demo

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

object Test {
  val shutdownMarker = "/tmp/spark-test/stop-spark/aaa"
  var stopFlag: Boolean = false

  def main(args: Array[String]) {
    val conf = new SparkConf().setAppName("stop spark streaming").setMaster("local[2]")

    val ssc = new StreamingContext(conf, Seconds(5))
    val file = ssc.textFileStream("/tmp/sparkstreaming")
    val res = file.map { line =>
      val arr = line.split("\t")
      arr(0) + "\t" + arr(2)
    }
//    res.saveAsTextFiles("/tmp/stroage")
    res.print()

    ssc.start()
    //检查间隔毫秒
    val checkIntervalMillis = 5000
    var isStopped = false
    while (!isStopped) {
      println("calling awaitTerminationOrTimeout")
      //等待执行停止。执行过程中发生的任何异常都会在此线程中抛出，如果执行停止了返回true，
      //线程等待超时长，当超过timeout时间后，会监测ExecutorService是否已经关闭，若关闭则返回true，否则返回false。
//      isStopped = ssc.awaitTerminationOrTimeout(checkIntervalMillis)
      isStopped = ssc.awaitTerminationOrTimeout(checkIntervalMillis)
      if (isStopped) {
        println("confirmed! The streaming context is stopped. Exiting application...")
      } else {
        println("Streaming App is still running. Timeout...")
      }
      //判断文件夹是否存在
      checkShutdownMarker
      if (!isStopped && stopFlag) {
        println("stopping ssc right now")
        //第一个true：停止相关的SparkContext。无论这个流媒体上下文是否已经启动，底层的SparkContext都将被停止。
        //第二个true：则通过等待所有接收到的数据的处理完成，从而优雅地停止。
        ssc.stop(true, true)
        println("ssc is stopped!!!!!!!")
      }
    }
  }

  def checkShutdownMarker = {
    if (!stopFlag) {
      //开始检查hdfs是否有stop-spark文件夹
      val fs = FileSystem.get(new Configuration())
      //如果有返回true，如果没有返回false
      val path = new Path(shutdownMarker)
      stopFlag = fs.exists(path)
      fs.delete(path,true)
    }
  }
}

