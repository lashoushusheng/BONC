package test_demo.design_mode.abstractfactory.pizzastore.use

import test_demo.design_mode.abstractfactory.pizzastore.pizza.Pizza

import scala.io.StdIn
import scala.util.control.Breaks._

class OrderPizza(absFactory: AbsFactory) {

  var orderType:String=_
  var pizza:Pizza = _

  breakable{
    do{
      println("请输入pizza的类型,使用抽象工厂模式....")
      orderType = StdIn.readLine()
      pizza = absFactory.createPizza(orderType)
      if(pizza == null){
        break()
      }
      this.pizza.prepare()
      this.pizza.bake()
      this.pizza.cut()
      this.pizza.box()
    }while(true)
  }

}
