package test_demo.log_demo;

import java.io.IOException;
import java.util.logging.*;

public class JULTest {

    public static Logger log = Logger.getLogger("TestLog");  //获取日志对象

    public static void main(String[] args) throws IOException {

        log.setLevel(Level.ALL);//设置logger的日志级别为全部，默认输出所有级别日志信息

        log.setUseParentHandlers(false); //禁用日志原本处理类

        FileHandler fileHandler = new FileHandler("/root/works/src/BONC/app16/scala/ma/data/log/testJUL.log");
        fileHandler.setLevel(Level.ALL); //记录级别
        log.addHandler(fileHandler); //添加Handler

        log.info("info");    //信息日志
        log.warning("warning"); //警告日志
        log.log(Level.SEVERE,"server"); //严重日志
        log.fine("fine");
    }
}

