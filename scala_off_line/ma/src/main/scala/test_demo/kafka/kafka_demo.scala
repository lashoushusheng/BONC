package test_demo.kafka

import java.util.Properties

import org.apache.kafka.common.serialization.{StringDeserializer, StringSerializer}
import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.streaming.dstream.{DStream, InputDStream}
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.streaming.kafka010.KafkaUtils
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.{Seconds, StreamingContext}
import rtcompute.DStruct.GlobalParams
import org.apache.spark.broadcast.Broadcast
import rtcompute.DPublic.{KafkaSink, Utils}

object kafka_demo {
  def main(args: Array[String]): Unit = {
    // [Spark], 参数设置.
    val spark: SparkSession = SparkSession.builder()
      .master("local[2]")
      .appName("kafka_demo")
      .getOrCreate()

    val sc: SparkContext = spark.sparkContext
    sc.setLogLevel(GlobalParams.sys_log_level)

//    val ssc = new StreamingContext(
//      sc, Seconds(GlobalParams.spark_stream_interval_seconds)
//    )

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

//      ssc.sparkContext.broadcast(
//        KafkaSink[String, String](kafkaProducerConfig)
//      )
      KafkaSink[String, String](kafkaProducerConfig)
    }

//    val dStream: DStream[String] = get_stream_from_kafka(ssc)
//    dStream.print()

    // write to kafka

    for (i <- 1 to 100){
      kafkaProducer.send(
        GlobalParams.kafka_rtc_result_topic,
        value = "ha ha " + i
      )
    }


//    // [Spark].
//    ssc.start()
//    ssc.awaitTermination()
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
    stream.map( x=> x.value() )
  }
}
