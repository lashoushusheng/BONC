package rtcompute.RtcCompute

import java.util.Properties

import akka.actor.{Actor, ActorRef, ActorSystem, Props}
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
import test_demo.akka.actors.{AActor, BActor}

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}

class MaPredict_Compute extends Actor{

	val shutdownMarker = "/tmp/spark-test/stop-spark/aaa"
	var stopFlag: Boolean = false

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

//	override def preStart(): Unit = {
//		println("preStart being executed")
//		Mysql_MaPredict.predictUndoList.clear()
//		Mysql_MaPredict.get_undo_tasks()
//		MaPredict_Process.loadModel_GM(Mysql_MaPredict.predictUndoList(0))
//	}

	override def receive: Receive = {
		case "start" =>
			println("The compute is already running ")
			// [kafka], 取数据流.
			var dStream:DStream[String] = null
			dStream = get_stream_from_kafka(ssc)//.window(Seconds(30),Seconds(2))
			dStream.print

//			dStream.foreachRDD(rdd =>{
//				if (rdd.count() >= 15 ){
//					val rowsRDD: RDD[Row] = rdd.map(_.split(",")).filter(x => x.length==2)
//						.map(t => Row(t(0),t(1).toDouble))
//
//					val df: DataFrame = spark.createDataFrame(rowsRDD,Schema.grey_schema)
//					//				df.show()
//					val res: Row = MaPredict_Process.process(df.collect(), Mysql_MaPredict.predictUndoList(0).modelType)
//
//					var result = ""
//					if(res.getAs[Int](0) == 0){
//						result = res.getAs[DataFrame](1).toJSON.collectAsList.toString
//						//					result.show()
//						println(result)
//						kafkaProducer.value.send(
//							GlobalParams.kafka_rtc_result_topic,
//							value = result
//						)
//					}
//				}
//				else{
//					println("数据不足15条，无法计算")
//				}
//			})

			// [Spark].
			ssc.start()
//			ssc.awaitTermination()
			//检查间隔毫秒
			val checkIntervalMillis = 5000
			var isStopped = false
			while (!isStopped) {
				println("calling awaitTerminationOrTimeout")
				//等待执行停止。执行过程中发生的任何异常都会在此线程中抛出，如果执行停止了返回true，
				//线程等待超时长，当超过timeout时间后，会监测ExecutorService是否已经关闭，若关闭则返回true，否则返回false。
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
					//第一个true：停止相关的SparkContext。无论这个流媒体上下文是否已经启动，底层的SparkContext都将被停止。
					//第二个true：则通过等待所有接收到的数据的处理完成，从而优雅地停止。
					ssc.stop(true, true)
					println("ssc is stopped!!!!!!!")
				}
			}

		case "exit" =>
			println("received exit order, exit system")
			context.stop(self)
//			context.system.terminate()
	}

	def checkShutdownMarker = {
		if (!stopFlag) {
			//开始检查hdfs是否有stop-spark文件夹
			val fs = FileSystem.get(new Configuration())
			//如果有返回true，如果没有返回false
			val path = new Path(shutdownMarker)
			stopFlag = fs.exists(path)
			fs.delete(path)
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

object MaPredict_Main_akka {

	def main(args: Array[String]): Unit = {
		// create ActorSystem
		val actorfactory = ActorSystem("actorfactory")
		val PredictActorRef: ActorRef = actorfactory.actorOf(Props[MaPredict_Compute],"PredictActor")

		val shutdownMarker = "/tmp/spark-test/stop-spark/aaa"
		val fs = FileSystem.get(new Configuration())
		//如果有返回true，如果没有返回false
		val path = new Path(shutdownMarker)
		fs.create(path,true)
		val stopFlag = fs.exists(new Path(shutdownMarker))
		println(stopFlag)

		println("send start order")
		PredictActorRef ! "start"
		Thread.sleep(1000 * 10)
		fs.create(path,true)
		Thread.sleep(1000 * 5)
		PredictActorRef ! "exit"
		println("再次启动")
		PredictActorRef ! "start"
//		Thread.sleep(1000 * 5)
//		println("send stop!")
//		PredictActorRef ! "stop"
	}
}

/*******************离线*********************/
		//		while(true){
//			Mysql_MaPredict.predictUndoList.clear()
//
//			// [读取], 待处理训练任务.
//			Mysql_MaPredict.get_undo_tasks()
//
//			// [处理], 训练任务.
//			Mysql_MaPredict.predictUndoList.foreach(
//				x =>{
//					// [ma_predict表], 更新-训练状态为(0->1，未开始->进行中).
//					Mysql_MaPredict.update_predict_state(
//						predictId=x.predId, predictState=1
//					)
//
//					// （算法API）, 训练.
//					val ret: Integer = MaPredict_Process.process(x,x.modelType)
//
//					// [ma_predict表], 更新-训练状态为(1->2，进行中->已完成).
//					if (ret >= 0){  // 执行成功.
//						println("执行成功")
//						Mysql_MaPredict.update_predict_state(
//							predictId=x.predId, predictState=2
//						)
//					}
//					else{           // 执行失败.
//						Mysql_MaPredict.update_predict_state(
//							predictId=x.predId, predictState= -1
//						)
//					}
//				}
//			)
//
//			// 休眠等待n秒.
//			Thread.sleep(1000 * 5)
//		}

