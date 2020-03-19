package test_demo.spark_demo.rdd_demo

import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

object rdd_demo02 {
  def main(args: Array[String]): Unit = {
    val config: SparkConf = new SparkConf()
      .setMaster("local[*]")
      .setAppName("demo02")

    val sc = new SparkContext(config)
    sc.setLogLevel("error")

    sc.setCheckpointDir("CK")

    val rdd: RDD[Int] = sc.makeRDD(List(1,2,3,4,5,6,7,8),4)

    val mapRDD: RDD[(Int, Int)] = rdd.map((_,1))

//    mapRDD.checkpoint()
//
    val reduceRDD: RDD[(Int, Int)] = mapRDD.reduceByKey(_+_)
    reduceRDD.checkpoint()


    reduceRDD.foreach(println)
    println(reduceRDD.toDebugString)
    sc.stop()
  }
}
