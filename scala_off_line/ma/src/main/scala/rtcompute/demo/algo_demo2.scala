package rtcompute.demo

import com.bonc.interfaceRaw.IBGA_Model
import com.bonc.models.OptimizationGuidance_bdapp
import org.apache.spark.sql.{Row, SparkSession}

import scala.io.Source


object algo_demo2 {

	def main(args: Array[String]): Unit = {

		val spark  = SparkSession.builder()
			.master("local[2]")
			.appName("MAnalysis")
			.getOrCreate()
		println("111111111111")

//		var df1 = spark.read.json("E:\\code\\Athena\\taurus_开发_测试\\项目poc_模型分析16\\name.json")
//		println(df1)
//		println(df1.show())

		val vObj: IBGA_Model[Row] =
			new OptimizationGuidance_bdapp().asInstanceOf[IBGA_Model[Row]]  //构造类对象

		val inputFile = "data\\opti_gui_data\\optmodel_0813.csv"
		val trainSavePath: String = "data\\opti_gui_trainsavepath"
		var predictSavePath = "data\\opti_gui_predictsavepath\\"
		val jsonPath = "conf/opti_gui_json/params_1.json"

		val param = Source.fromFile(jsonPath).mkString

		vObj.train_task_commit(
			inputFile, param, trainSavePath
		)

	}

}
