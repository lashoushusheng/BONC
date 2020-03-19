package test_demo.spark_demo.rdd_demo

import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

object rdd_demo01 {
  def main(args: Array[String]): Unit = {
    val config: SparkConf = new SparkConf()
      .setMaster("local[*]")
      .setAppName("demo01")
      .set("spark.default.parallelism","16")


    val sc = new SparkContext(config)

    val listRDD: RDD[Int] = sc.makeRDD(1 to 10)

    val tupleRDD: RDD[(Int, String)] = listRDD.mapPartitionsWithIndex {
      case (num, datas) => {
        datas.map((_, "num:" + num))
      }
    }

    tupleRDD.collect().foreach(println)
  }

}
