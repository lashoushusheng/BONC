package test_demo.spark_demo

import org.apache.spark.SparkConf
import org.apache.spark.streaming.dstream.{DStream, ReceiverInputDStream}
import org.apache.spark.streaming.{Seconds, StreamingContext}

object SparkStreaming01_WordCount {
  def main(args: Array[String]): Unit = {
    val sparkConf: SparkConf = new SparkConf().setMaster("local[*]").setAppName("SparkStreaming01_WordCount")
    val streamingContext = new StreamingContext(sparkConf,Seconds(3))

    val socketDStream: ReceiverInputDStream[String] = streamingContext.socketTextStream("192.168.0.100",9999)

    val wordDStream: DStream[String] = socketDStream.flatMap(line=>line.split(" "))
    val mapDStream: DStream[(String, Int)] = wordDStream.map((_,1))
    val wordTosumDStream: DStream[(String, Int)] = mapDStream.reduceByKey(_+_)

    wordTosumDStream.print()

    streamingContext.start()
    streamingContext.awaitTermination()
  }

}
