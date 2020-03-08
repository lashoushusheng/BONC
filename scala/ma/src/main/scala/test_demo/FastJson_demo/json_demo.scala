package test_demo.FastJson_demo

import com.alibaba.fastjson.JSON
import com.alibaba.fastjson.serializer.SerializerFeature
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession

case class User(str: String, i: Int)

object json_demo {
  def main(args: Array[String]): Unit = {
    val spark: SparkSession = SparkSession.builder().master("local[2]").appName("FastJsonTest").getOrCreate()

    val arr = Array("tom:10", "bob:14", "hurry:9")
    val dataRdd = spark.sparkContext.parallelize(arr)

    val dataString = dataRdd.map(x => {
      val arr = x.split(":")
      val name = arr(0)
      val age = arr(1).toInt
      val u = User(name,age)
      u
    }).map(x => {
      JSON.toJSONString(x,SerializerFeature.WriteMapNullValue)  // 这里需要显示SerializerFeature中的某一个，否则会报同时匹配两个方法的错误
    })

    dataString.foreach(println)
  }
}
