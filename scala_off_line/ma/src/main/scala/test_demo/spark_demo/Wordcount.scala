package test_demo.spark_demo

import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

object Wordcount {
  def main(args: Array[String]): Unit = {

    val sparkConf: SparkConf = new SparkConf().setAppName("Wordcount").setMaster("local[2]")
    val sc = new SparkContext(sparkConf)

    val lines: RDD[String] = sc.textFile("data")

    val words: RDD[String] = lines.flatMap(_.split(" "))

    val wordToOne: RDD[(String, Int)] = words.map((_,1)).reduceByKey(_+_)
    wordToOne.foreach(println)
  }

}
