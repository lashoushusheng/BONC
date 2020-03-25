package test_demo.correlation

import com.bonc.interfaceRaw.IBGA_Model_5
import com.bonc.models.BoncCorrClassArr
import org.apache.log4j.{Level, Logger}
import org.apache.spark.SparkConf
import org.apache.spark.sql.{DataFrame, Row, SparkSession}

import scala.io.Source

object correlation_test {
  Logger.getLogger("org").setLevel(Level.ERROR)
  Logger.getLogger("org.apache.spark").setLevel(Level.ERROR)
  Logger.getLogger("org.apache.hadoop").setLevel(Level.WARN)

  val conf: SparkConf = new SparkConf().set("spark.driver.memory", "2g")
    .set("spark.executor.memory", "2g")
    .setAppName("KAD").setMaster("local[*]")
  val spark: SparkSession = SparkSession.builder().config(conf).getOrCreate()
  def main(args: Array[String]): Unit = {
    //===========数据文件路径==========
    val filePath = "data/correlation/corr_1.csv"

    //===========参数文件路径==========（可以不用管）
    val jsonPath = "data/correlation/corrJson.json"

    //============结果保存路径===========
    val resultFilePath ="data/correlation/corr_result"   //本地

    var tp = 0//tp = 1，则进行训练阶段，需要指定好1：数据文件（utf-8)路径,2：参数文件路径，及对应的参数，3：模型训练结果保存的路径（预测时应与该值一致）
    //tp = 0,则进行预测阶段，需要指定好1：预测数据文件（utf-8)路径,2：参数文件路径，及对应的参数(与训练一致），3：模型训练结果保存的路径（与训练时保存路径一致）

    val Corr: IBGA_Model_5[Row] = new BoncCorrClassArr().asInstanceOf[IBGA_Model_5[Row]] //构造类对象
    if (tp == 1) {
      val param: String = Source.fromFile(jsonPath).mkString
      println(param)
      Corr.train_task_commit(filePath, param, resultFilePath)
    }else {
      Corr.loadModel(resultFilePath)
      val df: DataFrame = spark.read.option("header", value = true).option("inferSchema", value = true).csv(filePath)
      Corr.predict(df.collect())
    }


    //    if (tp == 1) {
    //      val param = Source.fromFile(jsonPath).mkString
    //      println(param)
    //      Corr.train_task_commit(filePath, param, resultFilePath)
    //    }else {
    //      Corr.loadModel(resultFilePath)
    //      val df = spark.read.option("header", true).option("inferSchema", true).csv(filePath)
    //      Corr.predict(df.collect())
    //    }
  }
}
