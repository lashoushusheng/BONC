package test_demo.spark_demo

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

object SparkSQL01_Demo {
  def main(args: Array[String]): Unit = {

    val spark = SparkSession
      .builder()
      .appName("SparkSQL01_Demo")
      .master("local[*]")
      .getOrCreate()

    // For implicit conversions like converting RDDs to DataFrames
    import spark.implicits._

    val frame = spark.read.json("/root/works/spark/examples/src/main/resources/people.json")
//    frame.show()

    frame.createOrReplaceTempView("user")

    spark.sql("select * from user").show()

    spark.stop()
  }


}
