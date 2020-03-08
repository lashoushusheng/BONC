package rtcompute.RtcCompute

import com.bonc.interfaceRaw.IBGA_Model_5
//import InterfaceRaw.{IBGA_Model, IBGA_Model_5}
import com.bonc.Model.GM_11_APP
import com.bonc.models.OptimizationGuidance_bdapp_5
import com.bonc.models.BoncRegression_app_5
import org.apache.spark.sql.Row
import rtcompute.DPublic.Utils
import rtcompute.DStruct.Item_MaTrain
import rtcompute.demo.OptimizationGuidanceMain_bdapp.spark

import scala.io.Source


object MaTrain_Process {

	/*
		模型训练.
	 */
	def process(iItem:Item_MaTrain,modelType:String): Integer ={

		// （算法API）构造类对象
		val OG_Model: IBGA_Model_5[Row] =
			new OptimizationGuidance_bdapp_5().asInstanceOf[IBGA_Model_5[Row]]

		// （软测量算法API）构造类对象
//		val SOFT_Model:IBGA_Model[Row] = new BoncRegression_app_5().asInstanceOf[IBGA_Model[Row]]
//		val GM: IBGA_Model_5[Row] = new GM_11_APP().asInstanceOf[IBGA_Model_5[Row]] //构造类对象

		// （训练参数）- 数据源文件.
//		val vDSDir = "E:\\code\\Athena\\taurus_开发_测试\\项目6_模型分析16\\2-2（魏工）jar包_1022\\jar包和数据_20191022"
//		val vDSFile = s"$vDSDir/optmodel_0813.csv"
		val vDSFile = s"${iItem.dsDir}/${iItem.dsFile}"
		println("vDSFile...............", vDSFile)
		val vOrgDF = spark.read.option("header", true).csv(vDSFile)
		println("vOrgDF...............", vOrgDF.count())

		// （训练参数）- 参数Json.
//		val vParamJsonDir = "E:\\code\\Athena\\taurus_开发_测试\\项目5_模型分析16\\2-2（魏工）jar包_1022\\jar包和数据_20191022"
//		val vParamJsonFile = "params_1.json"
//		val vParamJsonPath = s"$vParamJsonDir/$vParamJsonFile"
//		val vTrainParam = Source.fromFile(vParamJsonPath).mkString
//		println(s"[${Utils.now()}]: vParamJsonPath=[$vParamJsonPath]...vTrainParam=[$vTrainParam]")
		val vTrainParam = iItem.modelParams4ml
		println("vTrainParam...............", vTrainParam)

		// （训练参数）- 输出目录
//		val vTrainSavePath = "E:\\code\\Athena\\taurus_开发_测试\\项目6_模型分析16\\2-2（魏工）jar包_1022\\result"
		var vTrainSavePath = s"${iItem.trainDir}/train_result/"
		println("vTrainSavePath...............", vTrainSavePath)

		var ret = 1
		try{
			// （算法API）- 模型训练.
			modelType match {
				case "优化分析" => ret = OG_Model.train_task_commit(vDSFile, vTrainParam, vTrainSavePath)
//				case "产品质量软测量" => ret = SOFT_Model.train_task_commit(vDSFile, vTrainParam, vTrainSavePath)
//				case "生产预警分析" => ret = GM.train_task_commit(vDSFile, vTrainParam, vTrainSavePath)
				case _ => println("未匹配到模型")
			}
			// 打印.调试.
			println(s"模型训练结束...id=[${iItem.trainId}][${iItem.modelName}]...训练结果=[$ret]")
		}
		catch{
			case ex: Throwable =>println("模型训练...found error, exception..."+ ex)
			return -1
		}
		// 返回.
		ret
	}

}
