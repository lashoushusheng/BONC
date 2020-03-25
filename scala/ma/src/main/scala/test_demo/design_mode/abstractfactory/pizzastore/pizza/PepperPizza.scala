package test_demo.design_mode.abstractfactory.pizzastore.pizza

class PepperPizza extends Pizza{
  override def prepare(): Unit = {
    this.name = "胡椒pizza"
    println(this.name + "preparing...")
  }
}
