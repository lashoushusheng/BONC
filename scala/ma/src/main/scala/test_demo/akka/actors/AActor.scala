package test_demo.akka.actors

import akka.actor.{Actor, ActorRef}

class AActor(actorRef: ActorRef) extends Actor{

  val bActorRef: ActorRef = actorRef

  override def receive: Receive = {
    case "start" =>
      println("AActor Attacks,start ok")
      self ! "fire"

    case "fire" =>
      // send message to B
      // there need hold BActorRef of BActor
      println("AActor(黄飞鸿) 厉害 看我佛山无影脚")
      Thread.sleep(1000)
      if (ActorCount.count < 10){
        println(ActorCount.count)
        bActorRef ! "fire"
        ActorCount.count += 1
      }
      else {
        println("累了 不打了 A")
        bActorRef ! "exit"
        context.stop(self) // exit actoref
        context.system.terminate() // exit actorsystem
      }
  }
}

object ActorCount{
  var count = 0
}