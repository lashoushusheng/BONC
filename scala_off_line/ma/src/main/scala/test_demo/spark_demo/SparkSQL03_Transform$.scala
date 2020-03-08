package test_demo.spark_demo

import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}

object SparkSQL03_Transform$ {
  def main(args: Array[String]): Unit = {

    val spark = SparkSession
      .builder()
      .appName("SparkSQL01_Demo")
      .master("local[*]")
      .getOrCreate()

    import spark.implicits._

    // create RDD
    val rdd: RDD[(Int, String, Int)] = spark.sparkContext.makeRDD(List((1,"zhangsan",20),(2,"lisi",30),(3,"wangwu",40)))

    // transform to DF
    val df: DataFrame = rdd.toDF("id","name","age")
    df.show()


//    // transform to DS
//    val ds:Dataset[User] = df.as[User]
//
//    // transform to DF
//    val df1 = ds.toDF()
//
//    // transform to RDD
//    val rdd1: RDD[Row] = df1.rdd
//
//    rdd1.foreach(row => {
//      println(row.getString(1))
//    })
//
//    spark.stop()
  }
}
case class User(id:Int,name:String,age:Int)

