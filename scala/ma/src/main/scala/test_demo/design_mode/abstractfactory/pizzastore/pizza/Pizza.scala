package test_demo.design_mode.abstractfactory.pizzastore.pizza

abstract class Pizza {
  var name:String = _
  def prepare()

  def cut(): Unit ={
    println(this.name + "cutting....")
  }

  def bake(): Unit ={
    println(this.name + "baking...")
  }

  def box(): Unit ={
    println(this.name + "boxing...")
  }
}

