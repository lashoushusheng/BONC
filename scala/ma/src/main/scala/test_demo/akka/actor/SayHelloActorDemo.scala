package test_demo.akka.actor

import akka.actor.{Actor, ActorRef, ActorSystem, Props}

class SayHelloActor extends Actor {
  val hello = "hello"
  // 1. The received method will be called by MailBox of Actor.
  override def receive: Receive = {
    case "hello" => println("received hello, respond hello too")
      Thread.sleep(1000*3)
    case "ok" => println("received ok, respond ok too")
    case "exit" =>
      println("received exit order, exit system")
      context.stop(self) // exit actoref
      context.system.terminate() // exit actorsystem
    case _ => println("not match anything")
  }
}

object SayHelloActorDemo {
  // 1. create an ActorSystem to use to create Actor
  private val actorFactory = ActorSystem("actorFactory")
  // 2. return ActorRef as Actor will be created.
  private val sayHelloActor: ActorRef = actorFactory.actorOf(Props[SayHelloActor],"sayHelloActor")

  def main(args: Array[String]): Unit = {
    sayHelloActor ! "hello"
    sayHelloActor ! "ok"
//    sayHelloActor ! "exit"
    sayHelloActor ! "hello"
    sayHelloActor ! "ok"

  }
}



















//class SayHelloActor extends Actor {
//  override def receive: Receive = {
//    case "hello" =>
//      println("Receive hello, respond hello too")
//      var a = 0;
//      // for 循环
//      for( a <- 1 to 10){
//        println( "Value of a: " + a );
//      }
//    case "ok" => println("Receive ok, respond ok too")
//    case "exit" =>
//      println("received exit order, exit system")
//      context.stop(self)
//      context.system.terminate()
//    case _ => println("no match")
//  }
//}
//
//object SayHelloActorDemo {
//  private val actoryFactory = ActorSystem("actoryFactory")
//  private val SayHelloActorRef:ActorRef = actoryFactory.actorOf(Props[SayHelloActor],"SayHelloActor")
//
//  def main(args: Array[String]): Unit = {
//    SayHelloActorRef ! "hello"
//    SayHelloActorRef ! "ok"
//    SayHelloActorRef ! "exit"
//  }
//}
