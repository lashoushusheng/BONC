package test_demo.kafka

import java.util.{Date, Properties}

import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.kafka.common.serialization.{StringDeserializer, StringSerializer}
import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, Dataset, SparkSession}
import org.apache.spark.streaming.StreamingContext
import org.apache.spark.streaming.dstream.{DStream, InputDStream}
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.streaming.kafka010.KafkaUtils
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import rtcompute.DPublic.{KafkaSink, Utils}
import rtcompute.DStruct.GlobalParams

case class User(time:String, prediction:String)

object software_res_2_kafka$ {
  def main(args: Array[String]): Unit = {
    // [Spark], 参数设置.
    val spark: SparkSession = SparkSession.builder()
      .master("local[2]")
      .appName("kafka_demo")
      .getOrCreate()

    import spark.implicits._

    val sc: SparkContext = spark.sparkContext
    sc.setLogLevel(GlobalParams.sys_log_level)

    // [kafka_Producer], 创建, 计算结果输出.
    val kafkaProducer: KafkaSink[String, String] = {
      val kafkaProducerConfig:Properties = {
        val p = new Properties()
        p.setProperty("bootstrap.servers", GlobalParams.kafka_url)
        p.setProperty("key.serializer", classOf[StringSerializer].getName)
        p.setProperty("value.serializer", classOf[StringSerializer].getName)
        p
      }
      println(s"[${Utils.now()}]: " + "Kafka producer init done!")

      KafkaSink[String, String](kafkaProducerConfig)
    }

    while (true){
      val df: DataFrame = spark.read.option("header",value = true).csv("/root/works/idata/ma16_data/产品质量软测量/质量软测量_2#B/predict_result/aa.csv")
      //    df.show()

      // transform to DS
      val ds:Dataset[User] = df.as[User]
      //    ds.show()

      val rdd: RDD[User] = ds.rdd

      rdd.foreach(row => {
        kafkaProducer.send(
          GlobalParams.kafka_rtc_result_topic,
          value =
            s"${row.time}," +        // nodeId
              s"${row.prediction}"
        )
      })
      // 休眠等待n秒.
      Thread.sleep(1000 * 5)
    }
  }

  /*
  [Kafka]， 数据流.
* */
  def get_stream_from_kafka(ssc:StreamingContext): DStream[String] ={

    // [Kafka], 参数设置.
    val kafkaParams: Map[String, Object] = Map[String, Object](
      "bootstrap.servers" -> GlobalParams.kafka_url,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "0001",
      "auto.offset.reset" -> "latest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val kafkaTopics: Array[String] = GlobalParams.kafka_topics

    // [Kafka], 流处理.
    val stream: InputDStream[ConsumerRecord[String, String]] = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](kafkaTopics, kafkaParams)
    )
    // 返回.
    stream.map(x=> x.value())
  }
}
