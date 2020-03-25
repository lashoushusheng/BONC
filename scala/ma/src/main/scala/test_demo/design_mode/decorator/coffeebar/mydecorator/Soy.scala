package test_demo.design_mode.decorator.coffeebar.mydecorator

import test_demo.design_mode.decorator.coffeebar.Drink

class Soy(obj: Drink) extends Decorator(obj) {
  setDescription("Soy")
  setPrice(1.5f)
}
