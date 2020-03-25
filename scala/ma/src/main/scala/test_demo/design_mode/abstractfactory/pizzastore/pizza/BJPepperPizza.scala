package test_demo.design_mode.abstractfactory.pizzastore.pizza

class BJPepperPizza extends Pizza {
  override def prepare(): Unit = {
    this.name = "Beijing Pizza"
  }
}
