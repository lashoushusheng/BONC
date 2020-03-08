package test_demo.akka.yellowchicken.server

import akka.actor.{Actor, ActorRef, ActorSystem, Props}
import com.typesafe.config.ConfigFactory

class YellowChickenServer extends Actor{
  override def receive: Receive = {
    case "start" => println("YellowChickenServer start working...")
  }
}

object YellowChickenServer extends App{

  val host = "127.0.0.1" //服务端ip地址
  val port = 9999
  //创建config对象,指定协议类型，监听的ip和端口
  val config = ConfigFactory.parseString(
    s"""
       |akka.actor.provider="akka.remote.RemoteActorRefProvider"
       |akka.remote.netty.tcp.hostname=$host
       |akka.remote.netty.tcp.port=$port
        """.stripMargin)

  // create ActorSystem
  val serverActorSystem = ActorSystem("Server",config)
  val yellowChickenServerRef: ActorRef = serverActorSystem
    .actorOf(Props[YellowChickenServer],"YellowChickenServer")

  yellowChickenServerRef ! "start"

}


