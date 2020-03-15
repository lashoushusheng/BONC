package rtcompute.RtcCompute

import java.util.Properties

import rtcompute.DIO.{Mysql_MaPredict, Mysql_MaTrain}
import rtcompute.DStruct.{GlobalParams, Schema}
import com.bitanswer.authorization.Authentication
import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.kafka.common.serialization.{StringDeserializer, StringSerializer}
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.SparkContext
import org.apache.spark.broadcast.Broadcast
import org.apache.spark.streaming.dstream.{DStream, InputDStream}
import org.apache.spark.streaming.kafka010.KafkaUtils
import org.apache.spark.streaming.{Seconds, StreamingContext}
import rtcompute.DPublic.{KafkaSink, Utils}
import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}
import org.apache.spark.rdd.RDD

import scala.collection.mutable.ArrayBuffer


object MaPredict_Main_soft {

  def main(args: Array[String]): Unit = {

    // license Authentication
    //		Authentication.login()

    // [Spark], 参数设置.
    val spark: SparkSession = SparkSession.builder()
      .master("local[2]")
      .appName("MAnalysis_Predict")
      .getOrCreate()

    import spark.implicits._

    val sc: SparkContext = spark.sparkContext
    sc.setLogLevel(GlobalParams.sys_log_level)

    val ssc = new StreamingContext(
      sc, Seconds(30)
    )

    // [kafka_Producer], 创建, 计算结果输出.
    val kafkaProducer: Broadcast[KafkaSink[String, String]] = {
      val kafkaProducerConfig:Properties = {
        val p = new Properties()
        p.setProperty("bootstrap.servers", GlobalParams.kafka_url)
        p.setProperty("key.serializer", classOf[StringSerializer].getName)
        p.setProperty("value.serializer", classOf[StringSerializer].getName)
        p
      }
      println(s"[${Utils.now()}]: " + "Kafka producer init done!")

      ssc.sparkContext.broadcast(
        KafkaSink[String, String](kafkaProducerConfig)
      )
    }

    // softMeasure data sourse
    // val src_Soft: DataFrame = spark.read.option("header",value = true).csv("/root/works/idata/ma16_data/origin_data/产品质量软测量/predic_data/2号软测量预测数据.csv")
    // df.show()

    //    加载多个模型
    Mysql_MaPredict.predictUndoList.clear()
    Mysql_MaPredict.get_undo_tasks(args)

//    Mysql_MaPredict.predictUndoList.foreach(
//      x => {
//        MaPredict_Process.loadModel_Soft(x)
//      }
//    )

    // [kafka], 取数据流.
    var dStream:DStream[String] = null
    dStream = get_stream_from_kafka(ssc)
//    dStream.print

    dStream.foreachRDD{rdd =>
      val rowsRDD: RDD[Row] = rdd.map(_.split(",")).filter(x => x.length>0)
        .map(t => Row.fromSeq(t))
      val df: DataFrame = spark.createDataFrame(rowsRDD,Schema.dfd_schema)
//			df.show(20,truncate = false)
      println(df.count())
      if (!df.isEmpty){
        var resultList = new ArrayBuffer[String]()
        Mysql_MaPredict.predictUndoList.foreach(
          x =>{
            MaPredict_Process.loadModel_Soft(x)
            val res: Row = MaPredict_Process.process(df.collect(), x.modelType)

            if(res.getAs[Int](0) == 0){
              val result: String = res.getAs[DataFrame](1).toJSON.collectAsList.toString
              val msg: String = Array(x.modelName,result,x.modelParams).mkString("##")
              println(msg)
              resultList.append(msg)
            }
          }
        )
        kafkaProducer.value.send(
          GlobalParams.kafka_rtc_result_topic_soft,
          value = resultList.mkString("**")
        )
      }
    }

    // [Spark].
    ssc.start()
    ssc.awaitTermination()
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

    val kafkaTopics: Array[String] = GlobalParams.kafka_topics_soft

    // [Kafka], 流处理.
    val stream: InputDStream[ConsumerRecord[String, String]] = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](kafkaTopics, kafkaParams)
    )
    // 返回.
    stream.map( x=> x.value())
  }
}







