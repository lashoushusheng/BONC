package test_demo.sparkmasterworker.worker

import akka.actor.{Actor, ActorRef, ActorSystem, Props}
import com.typesafe.config.ConfigFactory

class SparkWorker extends Actor{
  override def receive: Receive = {
    case "" => ""

  }
}

object SparkWorker{
  def main(args: Array[String]): Unit = {
    val WorkerHost = "127.0.0.1" //服务端ip地址
    val WorkerPort = 10001

    val MasterHost = "127.0.0.1" //服务端ip地址
    val MasterPort = 10005
    //创建config对象,指定协议类型，监听的ip和端口
    val config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider="akka.remote.RemoteActorRefProvider"
         |akka.remote.netty.tcp.hostname=127.0.0.1
         |akka.remote.netty.tcp.port=10002
        """.stripMargin)

    // create ActorSystem
    val SparkWorkerSystem = ActorSystem("SparkWorker",config)
  }
}
