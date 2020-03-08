package rtcompute.RtcCompute

import com.bonc.Model.GM_11_APP
import com.bonc.interfaceRaw.IBGA_Model_5
//import InterfaceRaw.{IBGA_Model, IBGA_Model_5}
import org.apache.spark.sql.DataFrame
import com.bonc.models.OptimizationGuidance_bdapp_5
import com.bonc.models.BoncRegression_app_5
import org.apache.spark.sql.Row
import rtcompute.DStruct.{Item_MaPredict, Item_MaTrain}

object MaPredict_Process {

	// （算法API）构造类对象
	val OG_Model: IBGA_Model_5[Row] =
		new OptimizationGuidance_bdapp_5().asInstanceOf[IBGA_Model_5[Row]]
	def loadModel_OG(iItem:Item_MaPredict): Unit ={
		// （预测参数）- 训练目录
		var vTrainSavePath = s"${iItem.trainDir}/train_result/"
		OG_Model.loadModel(vTrainSavePath)
	}


	// 构造类对象(产品质量软测量)
//	val SOFT_Model:IBGA_Model_5[Row] = new BoncRegression_app_5().asInstanceOf[IBGA_Model_5[Row]]
//
//	// 加载训练模型
//	def loadModel_Soft(iItem:Item_MaPredict): Unit ={
//		// （预测参数）- 训练目录
//		var vTrainSavePath = s"${iItem.trainDir}/train_result/"
//		SOFT_Model.loadModel(vTrainSavePath)
//	}

//	// 构造类对象(生产预警分析)
//	val GM: IBGA_Model_5[Row] = new GM_11_APP().asInstanceOf[IBGA_Model_5[Row]] //构造类对象
//
//	// 加载训练模型
//	def loadModel_GM(iItem:Item_MaPredict): Unit ={
//		// （预测参数）- 训练目录
//		var vTrainSavePath = s"${iItem.trainDir}/train_result/"
//		GM.loadModel(vTrainSavePath)
//	}

	def process(rows: Array[Row],modelType:String): Row ={
		var res: Row = null
		try {
			modelType match {
//				case "产品质量软测量" => res = SOFT_Model.predict(rows)
				case "优化分析" => res = OG_Model.predict(rows)
//				case "生产预警分析" => res = GM.predict(rows)
				case _ => println("未匹配到该模型")
			}
		}
		catch{
			case ex: Throwable =>println("模型预测...found error, exception..."+ ex)
		}

//		res.getAs[DataFrame](1).show
//		res.getAs[Int](0)
		res
	}

	/*
  模型预测.
 */
	//	def process(iItem:Item_MaPredict,modelType:String): Integer ={
	//
	//		// （算法API）构造类对象
	//		val OG_Model: IBGA_Model[Row] =
	//			new OptimizationGuidance_bdapp().asInstanceOf[IBGA_Model[Row]]
	//
	//		// （软测量算法API）构造类对象
	//		val SOFT_Model:IBGA_Model[Row] = new BoncRegression_app_2().asInstanceOf[IBGA_Model[Row]]
	//
	//		// （预测参数）- 预测输入文件.
	//		val vPredDataPath = s"${iItem.dsDir}/${iItem.dsFile}"
	//		println("vPredDataPath...............", vPredDataPath)
	//
	//		// （预测参数）- 训练目录
	//		var vTrainSavePath = s"${iItem.trainDir}/train_result/"
	//		println("vTrainSavePath...............", vTrainSavePath)
	//
	//		// （预测参数）- 预测输出目录
	//		var vPredictSavePath = s"${iItem.predictDir}/predict_result/"
	//		println("vPredictSavePath...............", vPredictSavePath)
	//
	//
	//		// （算法API）- 模型训练.
	//		var ret = 1
	//		try{
	//			modelType match {
	//				case "优化分析" => ret = OG_Model.predict(vPredDataPath, vTrainSavePath, vPredictSavePath)
	//				case "产品质量软测量" => ret = SOFT_Model.predict(vPredDataPath, vTrainSavePath, vPredictSavePath)
	//				case _ => println("未匹配到模型")
	//			}
	//
	//			// 打印.调试.
	//			println(s"模型预测结束...id=[${iItem.predId}][${iItem.modelName}]...训练结果=[$ret]")
	//		}
	//		catch{
	//			case ex: Throwable =>println("模型预测...found error, exception..."+ ex)
	//			return -1
	//		}
	//		// 返回.
	//		ret
	//	}

}
