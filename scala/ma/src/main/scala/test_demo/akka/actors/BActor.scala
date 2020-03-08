package test_demo.akka.actors

import akka.actor.Actor

class BActor extends Actor{
  override def receive: Receive = {
    case "fire" =>
      println("BActor(乔峰) 挺猛 看我降龙十八掌")
      Thread.sleep(1000)
      sender() ! "fire"

    case "exit" =>
      println("累了 不打了 B")
      Thread.sleep(1000*5)
      context.stop(self) // exit actoref
      context.system.terminate() // exit actorsystem
  }
}
