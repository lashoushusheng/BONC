package test_demo.akka.actors

import akka.actor.{ActorRef, ActorSystem, Props}

object ActorGame {
  def main(args: Array[String]): Unit = {
    // create ActorSystem
    val actorfactory = ActorSystem("actorfactory")

    val bActorRef: ActorRef = actorfactory.actorOf(Props[BActor],"bActor")
    val aActorRef: ActorRef = actorfactory.actorOf(Props(new AActor(bActorRef)), "aActor")

    aActorRef ! "start"

  }
}
