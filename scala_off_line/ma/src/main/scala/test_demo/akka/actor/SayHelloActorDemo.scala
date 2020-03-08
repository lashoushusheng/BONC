package test_demo.akka.actor

import akka.actor.{Actor, ActorRef, ActorSystem, Props}

class SayHelloActor extends Actor {
  override def receive: Receive = {
    case "hello" =>
      println("Receive hello, respond hello too")
      var a = 0;
      // for 循环
      for( a <- 1 to 10){
        println( "Value of a: " + a );
      }
    case "ok" => println("Receive ok, respond ok too")
    case "exit" =>
      println("received exit order, exit system")
      context.stop(self)
      context.system.terminate()
    case _ => println("no match")
  }
}

object SayHelloActorDemo {
  private val actoryFactory = ActorSystem("actoryFactory")
  private val SayHelloActorRef:ActorRef = actoryFactory.actorOf(Props[SayHelloActor],"SayHelloActor")

  def main(args: Array[String]): Unit = {
    SayHelloActorRef ! "hello"
    SayHelloActorRef ! "ok"
    SayHelloActorRef ! "exit"
  }
}
