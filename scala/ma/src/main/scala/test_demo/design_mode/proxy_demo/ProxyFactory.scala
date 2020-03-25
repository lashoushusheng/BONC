package test_demo.design_mode.proxy_demo

import java.lang.reflect.{InvocationHandler, Method, Proxy}

class ProxyFactory(target:Object) {

  def getProxyInstance: Object ={

    Proxy.newProxyInstance(target.getClass.getClassLoader,
      target.getClass.getInterfaces, new InvocationHandler {
        override def invoke(proxy: Any, method: Method, args: Array[AnyRef]): AnyRef = {
          println("jdk Proxy start")
          val value: AnyRef = method.invoke(target,args).asInstanceOf[IteacherDao]
          value
        }
      })
  }
}
