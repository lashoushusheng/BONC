package test_demo.akka.actor

import akka.actor.{Actor, ActorRef, ActorSystem, Props}

class SayHelloActor_A extends Actor {
  val hello = "hello"
  // 1. The received method will be called by MailBox of Actor.
  override def receive: Receive = {
    case "hello" =>
      while (true){
        println("received hello, respond hello too A")
        Thread.sleep(1000*2)
      }

    case "ok" => println("received ok, respond ok too")
    case "exit" =>
      println("received exit order, exit system")
      context.stop(self) // exit actoref
      context.system.terminate() // exit actorsystem
    case _ => println("not match anything")
  }
}

class SayHelloActor_B extends Actor {
  val hello = "hello"
  // 1. The received method will be called by MailBox of Actor.
  override def receive: Receive = {
    case "hello" =>
      while (true){
        println("received hello, respond hello too B")
        Thread.sleep(1000*1)
      }

    case "ok" => println("received ok, respond ok too")
    case "exit" =>
      println("received exit order, exit system")
      context.stop(self) // exit actoref
      context.system.terminate() // exit actorsystem
    case _ => println("not match anything")
  }
}

object SayHelloActorDemo1 {
  // 1. create an ActorSystem to use to create Actor
  private val actorFactory = ActorSystem("actorFactory")
  // 2. return ActorRef as Actor will be created.
  private val sayHelloActor_a: ActorRef = actorFactory.actorOf(Props[SayHelloActor_A],"sayHelloActor_A")
  private val sayHelloActor_b: ActorRef = actorFactory.actorOf(Props[SayHelloActor_B],"sayHelloActor_B")

  def main(args: Array[String]): Unit = {
    sayHelloActor_a ! "hello"
    sayHelloActor_b ! "hello"
    while (true){
      println("main")
      Thread.sleep(1000*1)
    }
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
