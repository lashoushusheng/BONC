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

case class predictRes(time:String, prediction:String)

object MaPredict_Main_grey {

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

//    Seconds(GlobalParams.spark_stream_interval_seconds
    val ssc = new StreamingContext(
      sc, Seconds(3)
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

    // GM data source
//    val src_GM: DataFrame = spark.read.option("header",value = true).option("inferSchema","true").csv("data/greypredict/test_low.csv")
//    src_GM.show()

    //    加载单个模型
    //    MaPredict_Process.loadModel_GM(Mysql_MaPredict.predictUndoList(0))
    //    val row: Row = MaPredict_Process.process(src_GM.collect(), "生产预警分析")
    //    val result = row.getAs[DataFrame](1)

    //    加载多个模型
    Mysql_MaPredict.predictUndoList.clear()
    Mysql_MaPredict.get_undo_tasks(args)

    Mysql_MaPredict.predictUndoList.foreach(
      x => {
        MaPredict_Process.loadModel_GM(x)
//        MaPredict_Process.process(src_GM.collect(), x.modelType)
      }
    )

    // [kafka], 取数据流.
    var dStream:DStream[String] = null
    dStream = get_stream_from_kafka(ssc).window(Seconds(45),Seconds(3))
//    dStream.print()

    dStream.foreachRDD(rdd =>{
      if (rdd.count() >= 15 ){
        val rowsRDD: RDD[Row] = rdd.map(_.split(",")).filter(x => x.length==2)
          .map(t => Row(t(0),t(1).toDouble))

        val df: DataFrame = spark.createDataFrame(rowsRDD,Schema.grey_schema)
        //				df.show()

        Mysql_MaPredict.predictUndoList.foreach(
          x =>{
            val res: Row = MaPredict_Process.process(df.collect(), x.modelType)

            var result = ""
            if(res.getAs[Int](0) == 0){
              result = res.getAs[DataFrame](1).toJSON.collectAsList.toString
              val msg: String = Array(result,x.modelName).mkString("##")
              println(msg)
              kafkaProducer.value.send(
                GlobalParams.kafka_rtc_result_topic_grey,
                value = msg
              )
            }
          }
        )

      }
      else{
        println("数据不足15条，无法计算")
      }
    })

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

    val kafkaTopics: Array[String] = GlobalParams.kafka_topics_grey

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


