package test_demo.design_mode.abstractfactory.pizzastore.pizza

class GreekPizza extends Pizza{
  override def prepare(): Unit = {
    this.name = "希腊pizza"
    println(this.name + "preparing...")
  }
}