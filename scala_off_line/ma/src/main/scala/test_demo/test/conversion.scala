package test_demo.test

object conversion {
  def main(args: Array[String]): Unit = {
//    testUTF8ToGBK
//    testGBKToUTF8
    println("test".hashCode)

    def testUTF8ToGBK = {
      println("-------------------[Test UTF8 To GBK]-------------------------")
      val strBytes: Array[Byte] = new String("中文").getBytes("UTF-8")
      println("strBytes: " + strBytes.mkString(" "))

      val strUTF8 = new String(strBytes, "UTF-8")
      println("strUTF8 Bytes: " + strUTF8.getBytes("UTF-8").mkString(" "))

      // 使用默认的字节数组长度
      val strGBK = new String(strUTF8.getBytes("GBK"), "GBK")
      //    // 或者 指定转为GBK的字节长度
      //    val strGBK = new String(strUTF8.getBytes("GBK"), 0, strUTF8.length()*2, "GBK")
      println("strGBK Bytes: " + strGBK.getBytes("GBK").mkString(" "))

      println("strUTF8: " + strUTF8)
      println("strGBK: " + strGBK)
    }

    def testGBKToUTF8 = {
      println("-------------------[Test GBK To UTF8]-------------------------")
      val strBytes: Array[Byte] = new String("中文").getBytes("GBK")
      println("strBytes: " + strBytes.mkString(" "))

      val strGBK = new String(strBytes, "GBK")
      println("strGBK Bytes: " + strGBK.getBytes("GBK").mkString(" "))

      //    // 1. 使用默认的字节数组长度
      //    val strUTF8 = new String(strGBK.getBytes("UTF-8"), "UTF-8")
      //    // 2. 或者 指定转为UTF-8的字节长度
      //    //    这种方式如果指定的字节数组小于UTF-8编码后的字节数组长度，会出现乱码
      //    val strUTF8 = new String(strGBK.getBytes("UTF-8"), 0, strGBK.length()*3, "UTF-8")
      // 3. （推荐）使用 UTF-8 编解码格式
      val strUTF8 = new String(strGBK.getBytes("UTF-8"), "UTF-8")
      println("strUTF8 Bytes: " + strUTF8.getBytes("UTF-8").mkString(" "))

      println("strGBK: " + strGBK)
      println("strUTF8: " + strUTF8)
    }
  }

}
