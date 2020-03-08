package test_demo.test

object helloWorld {
  def main(args: Array[String]): Unit = {
    //  while (true) {
    //      println("hello world!")
    //      Thread.sleep(1000*3)
    //    }
    //  }
//    args.foreach(println)
    for(item<-args){
      println(item)
    }
  }
}
