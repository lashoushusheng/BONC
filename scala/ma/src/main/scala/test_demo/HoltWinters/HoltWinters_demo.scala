package test_demo.HoltWinters

//import InterfaceRaw.IBGA_Model_5
import com.bonc.interfaceRaw.IBGA_Model_5
import com.bonc.models.Holt_Winters
import org.apache.log4j.{Level, Logger}
import org.apache.spark.SparkConf
import org.apache.spark.sql.{DataFrame, Row, SparkSession}

import scala.io.Source

object HoltWinters_demo {
  Logger.getLogger("org").setLevel(Level.ERROR)
  Logger.getLogger("org.apache.spark").setLevel(Level.ERROR)
  Logger.getLogger("org.apache.hadoop").setLevel(Level.WARN)

  val conf: SparkConf = new SparkConf().set("spark.driver.memory", "2g")
    .set("spark.executor.memory", "2g")
    .setAppName("KAD").setMaster("local[*]")
  val spark: SparkSession = SparkSession.builder().config(conf).getOrCreate()
  def main(args: Array[String]): Unit = {
    //下限
    val datapath="data/Holt_Winter/test_low.csv"
    val jsonfile="data/Holt_Winter/params_mt_1.json"
    //===========训练阶段还是预测阶段设置==========
    var tp = 1 //tp = 1，则进行训练阶段，需要指定好1：数据文件（utf-8)路径,2：参数文件路径，及对应的参数，3：模型训练结果保存的路径（预测时应与该值一致）
    //tp = 0,则进行预测阶段，需要指定好1：预测数据文件（utf-8)路径,2：参数文件路径，及对应的参数(与训练一致），3：模型训练结果保存的路径（与训练时保存路径一致）


    val savepath="data/Holt_Winter/modelresult/mubiao"
    val predictfile="data/predictfile"


    val Holt_Winter: IBGA_Model_5[Row] = new Holt_Winters().asInstanceOf[IBGA_Model_5[Row]] //构造类对象
    if (tp == 0) {
      val param: String = Source.fromFile(jsonfile).mkString
      Holt_Winter.train_task_commit(datapath, param, savepath)
    }else {
      Holt_Winter.loadModel(savepath)
      val df: DataFrame = spark.read.option("header", true).option("inferSchema", true).csv(datapath)
      Holt_Winter.predict(df.collect())
    }
  }
}
