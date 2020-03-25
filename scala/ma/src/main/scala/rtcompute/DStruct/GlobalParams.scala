package rtcompute.DStruct

import java.io.File

import org.ini4j.Config
import org.ini4j.Ini
import org.ini4j.Profile.Section

/*
	全局参数.
 */
object GlobalParams {

	val cfg: Config = new Config()
	cfg.setMultiSection(true)   // 设置Section允许出现重复

	val ini:Ini = new Ini()
	ini.setConfig(cfg)

	// 取环境变量（BONC_MA16_PATH），ini配置文件路径.
//	val CONFIG_FILE = "E:\\code\\Athena\\taurus\\poc_MAnalysis\\scala\\ma.ini"
	val ENV_MA_PATH: String = sys.env("BONC_MA16_PATH")
	val CONFIG_FILE = s"$ENV_MA_PATH/ma.ini"
	println(s"ENV_MA_PATH=[$ENV_MA_PATH]......CONFIG_FILE=[$CONFIG_FILE]")


	// 加载配置文件
	val file: File = new File(CONFIG_FILE)
	file.createNewFile()
	ini.load(file)


	/* * * * * * *  * * * * * * *  * * * * * * *
			[Mysql].参数.
	* * * * * * *  * * * * * * *  * * * * * * */
	var dbSection:Section  = ini.get("db")

	val dbHost:String = dbSection.get("DB_HOST").trim
	val dbPort:String = dbSection.get("DB_PORT").trim
	val dbUser:String = dbSection.get("DB_USER").trim
	val dbPasswd:String = dbSection.get("DB_PASSWD").trim
	val dbName:String = dbSection.get("DB_DBNAME").trim

	val mysql_url: String = ("jdbc:mysql://%s:%s/%s?user=%s&password=%s&useUnicode=true&characterEncoding=UTF-8"
		).format(dbHost, dbPort, dbName, dbUser, dbPasswd)
//	println(s"mysql_url......$mysql_url")


	/* * * * * * *  * * * * * * *  * * * * * * *
				[SYS].参数.
	* * * * * * *  * * * * * * *  * * * * * * */
	val sysSection:Section = ini.get("sys")
	val sys_log_level:String = sysSection.get("SYS_LOG_LEVEL").trim
	val sys_log_dir:String = sysSection.get("SYS_LOG_DIR").trim

	println(s"sys_log_level......$sys_log_level")

	/* * * * * * *  * * * * * * *  * * * * * * *
      [license].
* * * * * * *  * * * * * * *  * * * * * * */
	val license:Section = ini.get("license")
	val serial_number:String = license.get("SERIAL_NUMBER").trim

	/* * * * * * *  * * * * * * *  * * * * * * *
			[Kafka].参数.
* * * * * * *  * * * * * * *  * * * * * * */
	val kafkaSection:Section = ini.get("kafka")
	val kafka_url:String = kafkaSection.get("KAFKA_URL").trim

	val kafka_topics = Array(
		"ma16_src_opt"
	)

	val kafka_topics_soft = Array(
				"ma16_src_soft_measure"
	)

	val kafka_topics_grey = Array(
				"ma16_src_greyPredict"
	)

	val kafka_topics_holtWinters = Array(
		"ma16_src_holtWinters"
	)

	// [写 RTC实时计算结果数据], -> topic.
	val kafka_rtc_result_topic_soft = "ma16_res_soft_measure"
	val kafka_rtc_result_topic_grey = "ma16_res_greyPredict"
	val kafka_rtc_result_topic_holtWinters = "ma16_res_holtWinters"
	val kafka_rtc_result_topic = "ma16_res_opt"

	/* * * * * * *  * * * * * * *  * * * * * * *
			[Spark].参数.
* * * * * * *  * * * * * * *  * * * * * * */
	// Streaming处理，间隔时间, 单位(秒).
	//	val spark_stream_interval_seconds = 60      // 60秒，计算1次.
	val sparkSection:Section = ini.get("spark")
	val spark_stream_interval_seconds:Int = sparkSection.get("INTERVAL_SECONDS").toInt
  val grey_interval_seconds:Int = sparkSection.get("GREY_INTERVAL_SECONDS").toInt
	val windowDuration:Int = sparkSection.get("WINDOWDURATION").toInt
	val slideDuration:Int = sparkSection.get("SLIDEDURATION").toInt

  /* * * * * * *  * * * * * * *  * * * * * * *
    [greyPredict].参数.
* * * * * * *  * * * * * * *  * * * * * * */
  val greySection:Section = ini.get("greyPredict")
  val grey_history_datalength:Int = greySection.get("GREY_HISTORY_DATALENGTH").toInt
  val grey_predict_datalength:Int = greySection.get("GREY_PREDICT_DATALENGTH").toInt
}


