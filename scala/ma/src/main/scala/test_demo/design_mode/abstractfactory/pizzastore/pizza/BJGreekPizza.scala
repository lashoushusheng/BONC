package test_demo.design_mode.abstractfactory.pizzastore.pizza

class BJGreekPizza extends Pizza {
  override def prepare(): Unit = {
    this.name = "Beijing Greek"
  }
}
