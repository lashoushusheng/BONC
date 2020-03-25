package test_demo.design_mode.decorator.coffeebar.mydecorator

import test_demo.design_mode.decorator.coffeebar.Drink


class Milk(obj: Drink) extends Decorator(obj) {

  setDescription("Milk")
  setPrice(2.0f)
}
