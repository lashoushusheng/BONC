package rtcompute.RtcCompute

import org.apache.spark.sql.SparkSession
import rtcompute.DIO.Mysql_MaTrain
import rtcompute.DStruct.GlobalParams
import com.bitanswer.authorization.Authentication


object MaTrain_Main {

	def main(args: Array[String]): Unit = {

		// license Authentication
//		Authentication.login()
		// [Spark], 参数设置.
		val spark  = SparkSession.builder()
			.master("local[2]")
			.appName("MAnalysis_train")
			.getOrCreate()

		val sc = spark.sparkContext
		sc.setLogLevel(GlobalParams.sys_log_level)

		while(true){
			Mysql_MaTrain.trainUndoList.clear()

			// [读取], 待处理训练任务.
			Mysql_MaTrain.get_undo_tasks()

			// [处理], 训练任务.
			Mysql_MaTrain.trainUndoList.foreach( x =>{
					// [ma_train表], 更新-训练状态为(0->1，未开始->进行中).
					Mysql_MaTrain.update_train_state(
						trainId=x.trainId, trainState=1
					)

					// （算法API）, 训练.
					val ret = MaTrain_Process.process(x,x.modelType)


					// [ma_train表], 更新-训练状态为(1->2，进行中->已完成).
					if (ret >= 0){  // 执行成功.
						Mysql_MaTrain.update_train_state(
							trainId=x.trainId, trainState=2
						)
					}
					else{           // 执行失败.
						Mysql_MaTrain.update_train_state(
							trainId=x.trainId, trainState= -1
						)
					}
				}
			)

			// 休眠等待n秒.
			Thread.sleep(1000 * 5)
		}
	}
}

