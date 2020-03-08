package rtcompute.DIO

import java.sql.{Connection, DriverManager, ResultSet, Statement}

import rtcompute.DPublic.Utils
import rtcompute.DStruct.{GlobalParams, Item_MaPredict}

import scala.collection.mutable.ArrayBuffer


object Mysql_MaPredict {

	classOf[com.mysql.jdbc.Driver]

	val conn: Connection = DriverManager.getConnection(
		GlobalParams.mysql_url
	)

	val statement: Statement = conn.createStatement(
		ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY
	)

	// 变更记录列表.
	val predictUndoList = new ArrayBuffer[Item_MaPredict]()


	/*
		读取，预测表，0未开始状态(predictState=0).
	 */
	def get_undo_tasks() : Unit ={

		try {
//			val sql: String = "SELECT a.id predId, a.modelType modelType, a.modelName modelName,  " +
//				" a.trainId trainId, b.trainDir trainDir, a.predictDir predictDir,  " +
//				" a.dsId dsId, c.dsDir dsDir, c.dsFile dsFile, a.predictState predictState " +
//				" FROM ma_predict a, ma_train b, ma_data_source c " +
//				" WHERE a.trainId=b.id AND a.dsId=c.id " +
//				" AND a.state=1 AND b.state=1 AND c.state=1 AND a.predictState=0 " +
//				" AND a.modelType='优化分析' ORDER BY a.id "
//			println(s"[${Utils.now()}]: [get_undo_tasks.sql]=======> $sql")

//			优化分析实时(sparkstreaming)
			val sql: String = "SELECT a.id predId, a.modelType modelType, a.modelName modelName,  " +
				" a.trainId trainId, b.trainDir trainDir, a.predictDir predictDir,  " +
				" a.dsId dsId, a.predictState predictState ,c.paramOriJson paramOriJson" +
				" FROM ma_predict a, ma_train b, ma_data_source c " +
				" WHERE a.trainId=b.id AND b.dsId=c.id " +
				" AND a.state=1 AND b.state=1 AND c.state=1 AND a.predictState=0 " +
				" AND a.modelType='优化分析' ORDER BY a.id "
			println(s"[${Utils.now()}]: [get_undo_tasks.sql]=======> $sql")


//			软测量测试
//			val sql: String = "SELECT a.id predId, a.modelType modelType, a.modelName modelName,  " +
//				" a.trainId trainId, b.trainDir trainDir, a.predictDir predictDir,  " +
//				" a.dsId dsId, c.dsDir dsDir, c.dsFile dsFile, a.predictState predictState " +
//				" FROM ma_predict a, ma_train b, ma_data_source c " +
//				" WHERE a.trainId=b.id AND a.dsId=c.id " +
//				" AND a.state=1 AND b.state=1 AND c.state=1 " +
//				" AND a.modelType='产品质量软测量' AND a.modelName='test2' ORDER BY a.id "
//			println(s"[${Utils.now()}]: [get_undo_tasks.sql]=======> $sql")

			val rs: ResultSet = statement.executeQuery(sql)
			while (rs.next) {

				val item = Item_MaPredict(
					predId = rs.getInt("predId"),
					modelType = rs.getString("modelType"),
					modelName = rs.getString("modelName"),

					dsId = rs.getInt("dsId"),
//					dsDir = rs.getString("dsDir"),
//					dsFile = rs.getString("dsFile"),
					paramOriJson = rs.getString("paramOriJson"),

					trainId = rs.getInt("trainId"),
					trainDir = rs.getString("trainDir"),

					predictDir = rs.getString("predictDir"),
					predictState = rs.getInt("predictState")
				)

				// 插入列表.
				this.predictUndoList.append(item)

				// 打印调试.
				println(s"[${Utils.now()}]: [get_undo_tasks.item]===> $item")
			}
		}
		finally {
		}
	}

	/*
  读取，预测表，0未开始状态(predictState=0).
 */
	def get_undo_tasks_by_modelName(modelName:String) : Item_MaPredict ={
		try {
		//			优化分析实时(sparkstreaming)
			val sql: String = "SELECT a.id predId, a.modelType modelType, a.modelName modelName," +
				" a.trainId trainId, b.trainDir trainDir, a.predictDir predictDir,  " +
				" a.dsId dsId, a.predictState predictState ,c.paramOriJson paramOriJson" +
				" FROM ma_predict a, ma_train b, ma_data_source c " +
				" WHERE a.trainId=b.id AND b.dsId=c.id " +
				s" AND a.state=1 AND b.state=1 AND c.state=1 AND a.modelName='$modelName' "

			println(s"[${Utils.now()}]: [get_undo_tasks.sql]=======> $sql")

			val rs: ResultSet = statement.executeQuery(sql)
			while (rs.next){
				val item = Item_MaPredict(
					predId = rs.getInt("predId"),
					modelType = rs.getString("modelType"),
					modelName = rs.getString("modelName"),

					dsId = rs.getInt("dsId"),
					//					dsDir = rs.getString("dsDir"),
					//					dsFile = rs.getString("dsFile"),
					paramOriJson = rs.getString("paramOriJson"),

					trainId = rs.getInt("trainId"),
					trainDir = rs.getString("trainDir"),

					predictDir = rs.getString("predictDir"),
					predictState = rs.getInt("predictState")
				)
				// 插入列表.
				this.predictUndoList.append(item)
				// 打印调试.
//				println(s"[${Utils.now()}]: [get_undo_tasks.item]===> $item")
			}
			this.predictUndoList(0)
		}
		finally {
		}
	}
	/*
		[update]，更新-预测状态为(预测状态，0未开始，1进行中，2已完成).
	 */
	def update_predict_state(predictId:Integer, predictState:Integer) : Unit ={

		var sql = ""
		if(predictState == 1) {
			sql = s"UPDATE  ma_predict  SET predictState=$predictState, predictBeginTime=now() " +
				s"WHERE id=$predictId"
		}
		else if(predictState == 2 || predictState == -1){
			sql = s"UPDATE  ma_predict  SET predictState=$predictState, predictEndTime=now() " +
				s"WHERE  id=$predictId"
		}

		val rs = statement.executeUpdate(sql)

		println(s"[${Utils.now()}]: [ma_predict] update predictState=[$predictState]..." +
			s"predictId=[$predictId]...rs=[$rs].")
	}

//	/*
//		[update]，更新-预测状态为(1->2，进行中->已完成).
//		预测状态，0未开始，1进行中，2已完成
//	 */
//	def update_doing_2done(predictId:Int, state:Int) : Unit ={
//
//		val sql = s"UPDATE    SET =$state, predictEndTime=now() " +
//			s" WHERE  id=$predictId"
//
//		val rs = statement.executeUpdate(sql)
//		println(s"[${Utils.now()}]: [ma_predict] update predictState=2..." +
//			s"predictId=[$predictId]...state=[$state]...rs=[$rs].")
//	}


	/*
		Test Main.
	 */
	def main(args: Array[String]): Unit = {
//		this.get_undo_tasks()
		val item: Item_MaPredict = this.get_undo_tasks_by_modelName("多氟多2点_all")
		println(item)
	}
}

