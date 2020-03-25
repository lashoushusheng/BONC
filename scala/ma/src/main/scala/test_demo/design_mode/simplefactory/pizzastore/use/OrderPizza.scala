package test_demo.design_mode.simplefactory.pizzastore.use

import test_demo.design_mode.simplefactory.pizzastore.pizza.{GreekPizza, PepperPizza, Pizza, SimpleFactory}

import scala.io.StdIn
import scala.util.control.Breaks._

abstract class OrderPizza {
  var orderType:String=_
  var pizza:Pizza = _

  breakable{
    do{
      println("请输入pizza的类型")
      orderType = StdIn.readLine()
      pizza = createPizza(orderType)
      if(pizza == null){
        break()
      }
      this.pizza.prepare()
      this.pizza.bake()
      this.pizza.cut()
      this.pizza.box()
    }while(true)
  }

  def createPizza(str: String):Pizza
}
