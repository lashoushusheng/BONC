package test_demo.design_mode.decorator.coffeebar.mydecorator

import test_demo.design_mode.decorator.coffeebar.Drink

class Chocolate(obj: Drink) extends Decorator(obj) {

  super.setDescription("Chocolate")
  //一份巧克力3.0f
  super.setPrice(3.0f)

}
