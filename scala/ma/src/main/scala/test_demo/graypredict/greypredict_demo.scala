package test_demo.graypredict

import java.util

import InterfaceRaw.{IBGA_Model, IBGA_Model_5}
import com.bonc.Model.GM_11_APP
import org.apache.log4j.{Level, Logger}
import org.apache.spark.SparkConf
import org.apache.spark.sql.{DataFrame, Row, SparkSession}

import com.alibaba.fastjson.JSONObject

import scala.io.Source

object greypredict_demo {
  Logger.getLogger("org").setLevel(Level.ERROR)
  Logger.getLogger("org.apache.spark").setLevel(Level.ERROR)
  Logger.getLogger("org.apache.hadoop").setLevel(Level.WARN)

  def main(args: Array[String]): Unit = {
    val conf: SparkConf = new SparkConf().set("spark.driver.memory", "2g")
      .set("spark.executor.memory", "2g")
      .setAppName("KAD").setMaster("local[*]")
    val spark: SparkSession = SparkSession.builder().config(conf).getOrCreate()
    import spark.implicits._

    val datapath="data/greypredict/test_low.csv"
//    val datapath="data/greypredict/生产预警_训练数据.csv"
//    val jsonfile="data/greypredict/params_mt_simplify.json"
    val jsonfile="data/greypredict/params_mt_1_0.2.0.json"

    //===========训练阶段还是预测阶段设置==========
    var tp = 0 //tp = 1，则进行训练阶段，需要指定好1：数据文件（utf-8)路径,2：参数文件路径，及对应的参数，3：模型训练结果保存的路径（预测时应与该值一致）
    //tp = 0,则进行预测阶段，需要指定好1：预测数据文件（utf-8)路径,2：参数文件路径，及对应的参数(与训练一致），3：模型训练结果保存的路径（与训练时保存路径一致）

    val savepath="data/greypredict/modelresult/mubiao"
    val predictfile="data/greypredict/predictfile"

    val GM: IBGA_Model_5[Row] = new GM_11_APP().asInstanceOf[IBGA_Model_5[Row]] //构造类对象
    if (tp == 1) {
      val param = Source.fromFile(jsonfile).mkString
      GM.train_task_commit(datapath, param, savepath)
    }else {
      GM.loadModel(savepath)
//      GM.predict(datapath,savepath,predictfile)
//      GM.predict()
      val df: DataFrame = spark.read.option("header", true).option("inferSchema", true).csv(datapath)
//      while (true){
//        val res: Row = GM.predict(df.collect())
//      }
      val res: Row = GM.predict(df.collect())
      val result: DataFrame = res.getAs[DataFrame](1)
      println(res.getAs[Int](0))
//      result.show()
      val jsonStr = result.toJSON.collectAsList.toString
      println(jsonStr)

//      val json = new JSONObject()
//      json.put("result", jsonStr)
//      println(json.toJSONString)
    }
  }
}

