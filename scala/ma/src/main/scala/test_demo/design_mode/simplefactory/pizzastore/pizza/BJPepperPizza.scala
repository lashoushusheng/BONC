package test_demo.design_mode.simplefactory.pizzastore.pizza

class BJPepperPizza extends Pizza {
  override def prepare(): Unit = {
    this.name = "Beijing Pizza"
  }
}
