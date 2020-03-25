package test_demo.design_mode.proxy_demo

class TeacherDao extends IteacherDao {
  override def tech(): Unit = {
    println("in class")
  }
}
