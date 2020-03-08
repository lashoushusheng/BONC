package test_demo.spark_demo

import akka.actor.{Actor, ActorRef, ActorSystem, Props}
import org.apache.spark.sql.SparkSession
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.streaming.dstream.{DStream, ReceiverInputDStream}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import rtcompute.DStruct.GlobalParams


class SparkStreaming01_WordCount extends Actor{
  override def receive: Receive = {
    case "start" =>
      val spark: SparkSession = SparkSession.builder()
        .master("local[2]")
        .appName("MAnalysis_Predict")
        .getOrCreate()

      import spark.implicits._

      val sc: SparkContext = spark.sparkContext
      sc.setLogLevel(GlobalParams.sys_log_level)

      val ssc = new StreamingContext(
        sc, Seconds(2)
      )

      val socketDStream: ReceiverInputDStream[String] = ssc.socketTextStream("192.168.0.8",8888)

      val wordDStream: DStream[String] = socketDStream.flatMap(line=>line.split(" "))
      val mapDStream: DStream[(String, Int)] = wordDStream.map((_,1))
      val wordTosumDStream: DStream[(String, Int)] = mapDStream.reduceByKey(_+_)

      wordTosumDStream.print()

      ssc.start()
      ssc.awaitTermination()
  }
}

class SparkStreaming01_WordCount1 extends Actor{
  override def receive: Receive = {
    case "start" =>
      val spark: SparkSession = SparkSession.builder()
        .master("local[2]")
        .appName("MAnalysis_Predict")
        .getOrCreate()

      import spark.implicits._

      val sc: SparkContext = spark.sparkContext
      sc.setLogLevel(GlobalParams.sys_log_level)

      val ssc = new StreamingContext(
        sc, Seconds(2)
      )

      val socketDStream: ReceiverInputDStream[String] = ssc.socketTextStream("192.168.0.8",9998)

      val wordDStream: DStream[String] = socketDStream.flatMap(line=>line.split(" "))
      val mapDStream: DStream[(String, Int)] = wordDStream.map((_,1))
      val wordTosumDStream: DStream[(String, Int)] = mapDStream.reduceByKey(_+_)

      wordTosumDStream.print()

      ssc.start()
      ssc.awaitTermination()
  }
}

object main{
  val actorFactory = ActorSystem("actorFactory")
  // 2. return ActorRef as Actor will be created.
  val sparkActor: ActorRef = actorFactory.actorOf(Props[SparkStreaming01_WordCount],"sparkActor")
  val sparkActor1: ActorRef = actorFactory.actorOf(Props[SparkStreaming01_WordCount1],"sparkActor1")

  def main(args: Array[String]): Unit = {
    sparkActor ! "start"
    sparkActor1 ! "start"
  }
}
