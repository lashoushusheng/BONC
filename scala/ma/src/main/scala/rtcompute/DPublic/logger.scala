package rtcompute.DPublic

import java.util.logging.{ConsoleHandler, FileHandler, Formatter, Level, LogRecord, Logger, SimpleFormatter}
import rtcompute.DStruct.GlobalParams

object logger {

  val logger: Logger = Logger.getLogger("ma16_log111")
  logger.setLevel(Level.ALL)
//  logger.setUseParentHandlers(false) //禁用日志原本处理类

  val logFormatter: Formatter = new Formatter {
    override def format(record: LogRecord): String = ""
  }

  // 控制台
  val consoleHandler = new ConsoleHandler
  consoleHandler.setFormatter(logFormatter)
  logger.addHandler(consoleHandler)
  consoleHandler.setLevel(Level.ALL)

  // 文件
  val fileHandler = new FileHandler(s"${GlobalParams.sys_log_dir}/ma16.log",false)
  fileHandler.setFormatter(logFormatter)
  logger.addHandler(fileHandler)
  fileHandler.setLevel(Level.ALL)

  def main(args: Array[String]): Unit = {

    logger.info("test")
    logger.severe("test")
  }
}
