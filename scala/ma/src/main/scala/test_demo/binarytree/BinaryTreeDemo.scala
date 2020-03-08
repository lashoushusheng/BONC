package test_demo.binarytree

object BinaryTreeDemo {
  def main(args: Array[String]): Unit = {
    val root = new HeroNode(1,"宋江")
    val hero2 = new HeroNode(2,"吴用")
    val hero3 = new HeroNode(3,"卢俊义")
    val hero4 = new HeroNode(4,"林冲")
    val hero5 = new HeroNode(5,"关胜")

    root.left = hero2
    root.right = hero3

    hero3.left = hero5
    hero3.right = hero4

    val binaryTree = new BinaryTree
    binaryTree.root = root
    binaryTree.preOrder()
  }
}

class HeroNode(hNo:Int,hName:String){
  val no = hNo
  var name = hName
  var left:HeroNode = null
  var right:HeroNode = null

  def preOrder(): Unit ={
    printf("node info no=%d name=%s\n",no,name)
    if(this.left != null){
      this.left.preOrder()
    }
    if(this.right != null){
      this.right.preOrder()
    }
  }


}

class BinaryTree{
  var root:HeroNode = null
  def preOrder(): Unit ={
    if(root != null){
      root.preOrder()
    }else{
      println("binaryTree is null")
    }
  }
}
