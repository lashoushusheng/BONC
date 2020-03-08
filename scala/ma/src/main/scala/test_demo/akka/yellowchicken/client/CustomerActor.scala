package test_demo.akka.yellowchicken.client

import akka.actor.{Actor, ActorRef, ActorSelection, ActorSystem, Props}
import com.typesafe.config.ConfigFactory

class CustomerActor(serverHost:String,serverPort:Int) extends Actor{
  // define a YellowChickenServerRef
  var serverActorRef: ActorSelection = _

  override def preStart(): Unit = {
    println("preStart being executed")
    serverActorRef = context.actorSelection(s"akka.tcp://Server@${serverHost}:${serverPort}/user/YellowChickenServer")
    println("serverActorRef" + serverActorRef)
  }

  override def receive: Receive = {
    case "start" => println("The client is already running ")
  }
}

object CustomerActor extends App{
  val (clientHost, clientPort, serverHost, serverPort) = ("127.0.0.1",9990,"127.0.0.1",9999)

  //创建config对象,指定协议类型，监听的ip和端口
  val config = ConfigFactory.parseString(
    s"""
       |akka.actor.provider="akka.remote.RemoteActorRefProvider"
       |akka.remote.netty.tcp.hostname=$clientHost
       |akka.remote.netty.tcp.port=$clientPort
        """.stripMargin)

  val clientActorSystem = ActorSystem("client",config)
  val customerActorRef: ActorRef = clientActorSystem.actorOf(Props(new CustomerActor(serverHost,serverPort)),"CustomerActor")
  customerActorRef ! "start"
}