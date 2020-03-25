package test_demo.design_mode.proxy_demo

class TeacherDaoProxy(target:IteacherDao) extends IteacherDao {

  override def tech(): Unit = {
    println("Proxy start")
    target.tech()
    println("Proxy end")
  }
}
