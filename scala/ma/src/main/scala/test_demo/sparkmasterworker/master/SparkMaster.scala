package test_demo.sparkmasterworker.master

import akka.actor.{Actor, ActorRef, ActorSystem, Props}
import com.typesafe.config.{Config, ConfigFactory}

class SparkMaster extends Actor{
  override def receive: Receive = {
    case "start" => println("master server start...")
    null
  }
}

object SparkMaster{
  def main(args: Array[String]): Unit = {
    val config: Config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider="akka.remote.RemoteActorRefProvider"
         |akka.remote.netty.tcp.hostname=127.0.0.1
         |akka.remote.netty.tcp.port=10005
        """.stripMargin)

    val sparkMasterSystem: ActorSystem = ActorSystem("SparkMaster",config)

    val sparkMasterRef: ActorRef = sparkMasterSystem.actorOf(Props[SparkMaster],"SparkMaster")
    sparkMasterRef ! "start"
  }
}
