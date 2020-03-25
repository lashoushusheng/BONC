package test_demo.design_mode.abstractfactory.pizzastore.use

import test_demo.design_mode.abstractfactory.pizzastore.pizza.{GreekPizza, PepperPizza, Pizza}

class BJFactory extends AbsFactory {
  override def createPizza(t: String): Pizza = {
    var pizza:Pizza = null

    t match {
      case "greek" => pizza = new GreekPizza
      case "pepper" => pizza = new PepperPizza
      case _ => println("没有这种pizza")
    }
    pizza
  }
}
