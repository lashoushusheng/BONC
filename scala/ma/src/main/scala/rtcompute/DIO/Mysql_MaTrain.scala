package rtcompute.DIO

import java.sql.{Connection, DriverManager, ResultSet, Statement}

import rtcompute.DPublic.Utils
import rtcompute.DStruct.{GlobalParams, Item_MaTrain}

import scala.collection.mutable.ArrayBuffer


object Mysql_MaTrain {

	classOf[com.mysql.jdbc.Driver]

	val conn = DriverManager.getConnection(
		GlobalParams.mysql_url
	)

	val statement = conn.createStatement(
		ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY
	)

	// 变更记录列表.
	val trainUndoList = new ArrayBuffer[Item_MaTrain]()

	/*
		读取，训练表，0未开始状态(trainState=0).
	 */
	def get_undo_tasks() : Unit ={

		try {
			val sql: String = " SELECT  a.id id, a.modelType modelType, a.modelName modelName, " +
				" a.modelParams4ml modelParams4ml, a.dsId dsId, b.dsDir dsDir, b.dsFile dsFile, " +
				" a.trainDir trainDir, a.trainState trainState" +
				" FROM  ma_train a, ma_data_source b " +
//				" WHERE  a.dsId=b.id AND a.trainState=0  AND  a.id=2" +
				" WHERE  a.dsId=b.id AND a.trainState=0 " +
				" ORDER BY a.id "
			println(s"[${Utils.now()}]: [get_undo_tasks.sql]=======> $sql")

			// AND a.modelType='生产预警分析'
			val rs: ResultSet = statement.executeQuery(sql)
			while (rs.next) {

				val item = Item_MaTrain(
					trainId = rs.getInt("id"),
					modelType = rs.getString("modelType"),
					modelName = rs.getString("modelName"),
					modelParams4ml = rs.getString("modelParams4ml"),

					dsId = rs.getInt("dsId"),
					dsDir = rs.getString("dsDir"),
					dsFile = rs.getString("dsFile"),

					trainDir = rs.getString("trainDir"),
					trainState = rs.getInt("trainState")
				)

				// 插入列表.
				this.trainUndoList.append(item)
				// 打印调试.
				println(s"[${Utils.now()}]: [get_undo_tasks.item]===> $item")
			}
		}
		finally {
		}
	}


	/*
		[update]，更新-训练状态为 (训练状态，0未开始，1进行中，2已完成).
	 */
	def update_train_state(trainId:Integer, trainState:Integer) : Unit ={

		var sql = ""
		if(trainState == 1){
			sql = s"UPDATE  ma_train  SET trainState=$trainState, trainBeginTime=now() WHERE  id=$trainId"
		}
		else if(trainState == 2 || trainState == -1){
			sql = s"UPDATE  ma_train  SET trainState=$trainState, trainEndTime=now() WHERE  id=$trainId"
		}

		val rs: Int = statement.executeUpdate(sql)

		println(s"[${Utils.now()}]: [ma_train] update trainState=[$trainState]..." +
			s"trainId=[$trainId]...rs=[$rs].")
	}

//	/*
//		[update]，更新-训练状态为(1->2，进行中->已完成).
//		训练状态，0未开始，1进行中，2已完成
//	 */
//	def update_doing_2done(trainId:Int, state:Int) : Unit ={
//
//		val sql = s"UPDATE  ma_train  SET trainState=$state, =now() " +
//			s" WHERE  id=$trainId"
//
//		val rs = statement.executeUpdate(sql)
//		println(s"[${Utils.now()}]: [ma_train] update trainState=2..." +
//			s"trainId=[$trainId]...state=[$state]...rs=[$rs].")
//	}


	/*
		Test Main.
	 */
	def main(args: Array[String]): Unit = {
		this.get_undo_tasks()
	}
}
