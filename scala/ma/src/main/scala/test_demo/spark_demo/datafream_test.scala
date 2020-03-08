package test_demo.spark_demo

import org.apache.spark.sql.{Row, SparkSession}

object datafream_test extends App {
  val spark = SparkSession
    .builder()
    .appName("Spark SQL basic example")
    .master("local[2]")
    .getOrCreate()

  def circularProcess(line : Row) : Unit = {
    // 打印行里面的值，此处是获取第一列的值
    println(line)
  }

//  val df = spark.read.json("/root/works/spark/examples/src/main/resources/people.json")
//  df.foreach(circularProcess : Row => Unit)
  val a = spark.readStream.format("org.apache.bahir.sql.streaming.mqtt.MQTTStreamSourceProvider")
    .option("topic", "mytopic")
    .load("tcp://localhost:1883")

  println(a)
}
