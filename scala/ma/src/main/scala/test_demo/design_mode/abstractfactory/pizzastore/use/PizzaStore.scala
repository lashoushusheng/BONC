package test_demo.design_mode.abstractfactory.pizzastore.use

object PizzaStore {
  def main(args: Array[String]): Unit = {
    val orderPizza = new OrderPizza(new BJFactory)
    println("exit")
  }
}

