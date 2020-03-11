package rtcompute.RtcCompute

import java.util.Properties

import rtcompute.DIO.{Mysql_MaPredict, Mysql_MaTrain}
import rtcompute.DStruct.{GlobalParams, Item_MaPredict, Schema}
import com.bitanswer.authorization.Authentication
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}
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


object MaPredict_Main_opt {
	val shutdownMarker = "/tmp/spark-test/stop-spark/stop"
	var stopFlag: Boolean = false
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
			sc, Seconds(GlobalParams.spark_stream_interval_seconds)
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

		// dfd data sourse
//		val dfd_src: DataFrame = spark.read.option("header",value = true).csv("/root/works/idata/ma16_data/origin_data/产品质量软测量/predic_data/2号软测量预测数据.csv")
//		dfd_src.show()

		val item: Item_MaPredict = Mysql_MaPredict.get_undo_tasks_by_modelName(args(0))
		MaPredict_Process.loadModel_OG(item)

//		// [kafka], 取数据流.
		var dStream:DStream[String] = null
		dStream = get_stream_from_kafka(ssc)
//		dStream.print

		dStream.foreachRDD{rdd =>
			val rowsRDD: RDD[Row] = rdd.map(_.split(",")).filter(x => x.length==99)
				.map(t => Row.fromSeq(t))
			val df: DataFrame = spark.createDataFrame(rowsRDD,Schema.dfd_schema)

			val res: Row = MaPredict_Process.process(df.collect(), item.modelType)
			val ret: Int = res.getAs[Int](0)
			val resultDF: DataFrame =  res.getAs[DataFrame](1)
			if(ret == 0 && !resultDF.isEmpty){
				val result: String = resultDF.toJSON.collectAsList.toString
				val paramOriJson: String = item.paramOriJson
				val msg: String = Array(result,paramOriJson).mkString("##")

				println(msg)

				kafkaProducer.value.send(
					GlobalParams.kafka_rtc_result_topic,
					value = msg
				)
			}
		}
		// [Spark].
		ssc.start()
//		ssc.awaitTermination()
		//检查间隔毫秒
		val checkIntervalMillis = 10000
		var isStopped = false
		while (!isStopped) {
			println("calling awaitTerminationOrTimeout")
			isStopped = ssc.awaitTerminationOrTimeout(checkIntervalMillis)
			if (isStopped) {
				println("confirmed! The streaming context is stopped. Exiting application...")
			} else {
				println("Streaming App is still running. Timeout...")
			}
			//判断文件夹是否存在
			checkShutdownMarker
			if (!isStopped && stopFlag) {
				println("stopping ssc right now")
				ssc.stop(true, false)
				println("ssc is stopped!!!!!!!")
			}
		}
	}

	def checkShutdownMarker: AnyVal = {
		if (!stopFlag) {
			//开始检查hdfs是否有stop-spark文件夹
			val fs: FileSystem = FileSystem.get(new Configuration())
			//如果有返回true，如果没有返回false
			val path = new Path(shutdownMarker)
			stopFlag = fs.exists(path)
			fs.delete(path,true)
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
		stream.map( x=> x.value())
	}
}
