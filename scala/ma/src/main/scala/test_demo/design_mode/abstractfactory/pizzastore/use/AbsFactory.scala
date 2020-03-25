package test_demo.design_mode.abstractfactory.pizzastore.use

import test_demo.design_mode.abstractfactory.pizzastore.pizza.Pizza

trait AbsFactory {
  def createPizza(t:String):Pizza
}
