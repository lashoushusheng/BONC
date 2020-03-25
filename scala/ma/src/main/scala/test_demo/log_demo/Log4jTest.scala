package test_demo.log_demo

import org.apache.log4j.Logger

object Log4jTest {
  def main(args: Array[String]): Unit = {
    val aaLogger: Logger = Logger.getLogger("aa")
    aaLogger.info("hello")
  }

}
