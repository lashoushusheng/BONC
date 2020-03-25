package test_demo.design_mode.simplefactory.pizzastore.pizza

import scala.io.StdIn
import scala.util.control.Breaks.{break, breakable}

object SimpleFactory {
  def createPizza(t:String): Pizza ={
    var pizza:Pizza = null

    t match {
      case "greek" => pizza = new GreekPizza
      case "pepper" => pizza = new PepperPizza
      case _ => println("没有这种pizza")
    }
    pizza
  }
}
