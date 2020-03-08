package test_demo.accompany

object ChildJoinGame {
  def main(args: Array[String]): Unit = {
    val child1 = new Child03("1")
    val child2 = new Child03("2")
    Child02.joinGame(child1)
    Child02.joinGame(child2)
    Child02.showNum()
  }
}

class Child03(cname:String){
  var name: String = cname
}

object Child02{
  var totalChildNum = 0

  def joinGame(child:Child03): Unit ={
    printf("%s join games\n", child.name)
    totalChildNum += 1
  }

  def showNum(): Unit ={
    printf("there are %d children playing games\n", totalChildNum)
  }
}
