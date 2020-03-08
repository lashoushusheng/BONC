package rtcompute.RtcCompute

import org.apache.spark.sql.SparkSession
import rtcompute.DIO.{Mysql_MaPredict, Mysql_MaTrain}
import rtcompute.DStruct.GlobalParams
import com.bitanswer.authorization.Authentication
import org.apache.spark.SparkContext

object MaPredict_Main {

	def main(args: Array[String]): Unit = {

		// license Authentication
//		Authentication.login()

		// [Spark], 参数设置.
		val spark: SparkSession = SparkSession.builder()
			.master("local[2]")
			.appName("MAnalysis_Predict")
			.getOrCreate()
		import spark.implicits._

		val sc: SparkContext = spark.sparkContext
		sc.setLogLevel(GlobalParams.sys_log_level)

		/****************************************/
		Mysql_MaPredict.predictUndoList.clear()
		Mysql_MaPredict.get_undo_tasks()
		while(true){
			Mysql_MaPredict.predictUndoList.clear()

			// [读取], 待处理训练任务.
			Mysql_MaPredict.get_undo_tasks()

			// [处理], 训练任务.
			Mysql_MaPredict.predictUndoList.foreach(
				x =>{
					// [ma_predict表], 更新-训练状态为(0->1，未开始->进行中).
					Mysql_MaPredict.update_predict_state(
						predictId=x.predId, predictState=1
					)

					// （算法API）, 训练.
					val ret: Integer = MaPredict_Process.process(x,x.modelType)

					// [ma_predict表], 更新-训练状态为(1->2，进行中->已完成).
					if (ret >= 0){  // 执行成功.
						println("执行成功")
						Mysql_MaPredict.update_predict_state(
							predictId=x.predId, predictState=2
						)
					}
					else{           // 执行失败.
						Mysql_MaPredict.update_predict_state(
							predictId=x.predId, predictState= -1
						)
					}
				}
			)
			// 休眠等待n秒.
			Thread.sleep(1000 * 5)
		}
	}
}

