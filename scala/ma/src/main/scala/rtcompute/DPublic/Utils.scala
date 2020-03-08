package rtcompute.DPublic

import java.text.SimpleDateFormat
import java.util.Date

object Utils {

	/*
		当前时间.
	*/
	def now(): String = {
		val now: Date = new Date()
		val dateFormat: SimpleDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
		val date:String = dateFormat.format(now)
		date
	}



	def main(args: Array[String]): Unit = {
		val now: String = this.now()
		println(s"[$now]: ")
	}
}
