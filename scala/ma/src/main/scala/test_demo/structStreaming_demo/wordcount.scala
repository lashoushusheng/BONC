package test_demo.structStreaming_demo

import org.apache.spark.sql.streaming.StreamingQuery
import org.apache.spark.sql.{DataFrame, SparkSession}

object wordcount {
  def main(args: Array[String]): Unit = {
    val spark: SparkSession = SparkSession.builder()
      .master("local[2]")
      .appName("MAnalysis_train")
      .getOrCreate()

    import spark.implicits._

    // 1. load data
    val lines: DataFrame = spark.readStream.format("socket")
      .option("host", "master")
      .option("port", 9999)
      .load()

    // 2. output
    val result: StreamingQuery = lines.writeStream.format("console")
      .outputMode("update")
      .start

    result.awaitTermination()
  }
}
