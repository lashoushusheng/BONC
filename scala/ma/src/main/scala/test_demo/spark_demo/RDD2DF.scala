package test_demo.spark_demo

import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import org.apache.spark.sql.types.{StringType, StructField, StructType}

case class Order(id:String,name:String,commodity:String,age:String,date:String)

object RDD2DF {
  def main(args: Array[String]): Unit = {
    val spark: SparkSession = SparkSession.builder()
      .appName("DFDemo")
      .master("local")
      .getOrCreate()

    val stuRDD: RDD[String] = spark.sparkContext.textFile("/root/works/src/git_test/rtc/poc_MAnalysis/scala/ma/src/main/scala/test_demo/spark_demo/student.txt")
//    import spark.implicits._

    val schemaString = "id,name,age"
    val fields: Array[StructField] = schemaString.split(",").map(fieldName => StructField(fieldName, StringType, nullable = true))
    val schema = StructType(fields)

    val rowRDD: RDD[Row] = stuRDD.map(_.split(",")).map(parts⇒Row(parts(0),parts(1),parts(2)))
    val stuDf: DataFrame = spark.createDataFrame(rowRDD, schema)

    stuDf.show()


    spark.stop()
  }
}
