package test_demo.design_mode.decorator.coffeebar.mydecorator

import test_demo.design_mode.decorator.coffeebar.Drink


class NewMilk(obj: Drink) extends Decorator(obj) {

  setDescription("新式Milk")
  setPrice(4.0f)
}