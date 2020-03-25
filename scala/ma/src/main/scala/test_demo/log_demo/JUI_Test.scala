package test_demo.log_demo

import java.util.logging.{ConsoleHandler, FileHandler, Formatter, Level, LogRecord, Logger, SimpleFormatter}

object JUI_Test {
  def main(args: Array[String]): Unit = {
    val logger: Logger = Logger.getLogger("ma16_log")

    val logFormatter: Formatter = new Formatter {
      override def format(record: LogRecord): String = ""
    }

    // 控制台
    val consoleHandler = new ConsoleHandler
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    logger.setLevel(Level.INFO)
    consoleHandler.setLevel(Level.INFO)

    // 文件
    val fileHandler = new FileHandler("/tmp/log/1111ul.log",false)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    logger.info("start")
    logger.info("end")
  }
}
