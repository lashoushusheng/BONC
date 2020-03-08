package rtcompute.demo

import java.text.SimpleDateFormat

//import com.bonc.interfaceRaw.IBGA_Model
//import com.bonc.models.OptimizationGuidance_bdapp
import com.bonc.utils.df2schemaUtils
import org.apache.log4j.{Level, Logger}
import org.apache.spark.SparkConf
import org.apache.spark.sql.{Row, SparkSession}

import scala.collection.mutable.ArrayBuffer
import scala.io.Source

/**
 * Created by yongchaowei on 2018/8/13.
 */
object OptimizationGuidanceMain_bdapp {

  Logger.getLogger("org").setLevel(Level.WARN)
  Logger.getLogger("org.apache.spark").setLevel(Level.WARN)
  Logger.getLogger("org.apache.hadoop").setLevel(Level.WARN)
  var train_result = -1
  var savemodel_result = -1
  var loadmodel_result = -1

  val conf = new SparkConf().setAppName("OptimizationGuidance").setMaster("local[*]")

  val spark = SparkSession.builder().config(conf).getOrCreate()
  def main(args: Array[String]): Unit = {



//    val Opt_Gui: IBGA_Model[Row] = new OptimizationGuidance_bdapp().asInstanceOf[IBGA_Model[Row]] //构造类对象

    val inputfile = "data\\opti_gui_data\\optmodel_0813.csv"

    val org_df = spark.read.option("header", true).csv(inputfile)

    println(org_df.count())

    import spark.implicits._
    //    val df_m = org_df.map(x => {
    //      (convertDateStr2TimeStamp(x.getAs[String]("time"), "yyyy/MM/dd HH:mm"),
    //        x.getAs[String]("time"))
    //    }).toDF("time1", "time2")
    //
    //    val df = df2schemaUtils.df2schema(org_df.join(df_m, org_df("time") === df_m("time2")).drop("time2", "time").withColumnRenamed("time1", "time"))


    val trainSavePath: String = "data\\opti_gui_trainsavepath"
    var predictSavePath = "data\\opti_gui_predictsavepath\\"
    val json_path = "conf/opti_gui_json/params_1.json"
    var tp = 1 //1预测，0是训练

//    if (tp == 0) {
//
//      //参数设置和传递
//      val param = Source.fromFile(json_path).mkString
//      Opt_Gui.train_task_commit(inputfile,param,trainSavePath)
//    } else {
//      var predictDataPath = "data\\opti_gui_data\\optmodel_0814.csv"
//
//      val param = Source.fromFile(json_path).mkString
//      Opt_Gui.predict(predictDataPath,trainSavePath,predictSavePath)
//
//    }
  }

  //  //日期格式转化为时间戳
  //  def convertDateStr2TimeStamp(dateStr: String, pattern: String): Long = {
  //    new SimpleDateFormat(pattern).parse(dateStr).getTime/1000
  //  }
}

