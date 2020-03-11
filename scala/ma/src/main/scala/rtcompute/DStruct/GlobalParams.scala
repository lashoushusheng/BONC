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
//		"ma16_src_soft_measure"
//		"ma16_src_greyPredict"
		"ma16_src_opt"
	)

	// [写 RTC实时计算结果数据], -> topic.
//	val kafka_rtc_result_topic = "ma16_res_soft_measure"
//	val kafka_rtc_result_topic = "ma16_res_greyPredict"
	val kafka_rtc_result_topic = "ma16_res_opt"


	/* * * * * * *  * * * * * * *  * * * * * * *
			[Spark].参数.
* * * * * * *  * * * * * * *  * * * * * * */
	// Streaming处理，间隔时间, 单位(秒).
	//	val spark_stream_interval_seconds = 60      // 60秒，计算1次.
	val sparkSection:Section = ini.get("spark")
	val spark_stream_interval_seconds:Int = sparkSection.get("INTERVAL_SECONDS").toInt

	val colNames = Array("time",
		"AFIC_3001_F03_MV",
		"AFIC_3002_F03_MV",
		"AFIC_3003_F03_MV",
		"AFIC_3005_F03_MV",
		"AFIC_3006_F03_MV",
		"AFIC_3007_F03_MV",
		"AFIC_3020_F03_MV",
		"AFIC_3021_F03_MV",
		"AFIC0302_F03",
		"AFIC0304_F03",
		"AFIC0305_F03",
		"AFIQ0306_F03",
		"AMIC_C301_F03_MV",
		"AMIC_C302_F03_MV",
		"AMIC_L303_F03_MV",
		"AMII_C301_F03",
		"AMII_C302_F03",
		"AMIIL303_F03",
		"APIA0303_F03",
		"APIA0304_F03",
		"APIA0307_F03",
		"APIA0308_F03",
		"APIR0305_F03",
		"APIR0321_F03",
		"APIRA0311_F03",
		"APIRA0312_F03",
		"APIRA0314_F03",
		"ATI0301_F03",
		"ATI0319_F03",
		"ATI0320_F03",
		"ATI0321_F03",
		"ATIR0302_F03",
		"ATIR0303_F03",
		"ATIR0304_F03",
		"ATIR0305_F03",
		"ATIR0306_F03",
		"ATIR0307_F03",
		"ATIR0308_F03",
		"ATIR0309_F03",
		"ATIR0310_F03",
		"ATIR0311_F03",
		"ATIR0312_F03",
		"ATIR0313_F03",
		"ATIR0314_F03",
		"ATIR0315_F03",
		"ATIR0316_F03",
		"FEED_SK03_F03",
		"PIA0302_F03",
		"TI0318_F03",
		"SETPOINT03_F03",
		"BFIC_3021_F03_MV",
		"BFIC0304_F03",
		"BMII_C301_F03",
		"BFIC0305_F03",
		"BMIC_C301_F03_MV",
		"BFIC_3020_F03_MV",
		"BFIC_3005_F03_MV",
		"BFIC_3001_F03_MV",
		"BFIC0302_F03",
		"BFIC_3003_F03_MV",
		"BFIC_3007_F03_MV",
		"BFIQ0306_F03",
		"BMIC_L303_F03_MV",
		"BPIA0303_F03",
		"BMII_C302_F03",
		"BTIR0302_F03",
		"BPIA0308_F03",
		"BFIC_3006_F03_MV",
		"BTIR0304_F03",
		"BMIC_C302_F03_MV",
		"BMIIL303_F03",
		"BPIA0304_F03",
		"BPIA0307_F03",
		"BPIR0305_F03",
		"BPIR0321_F03",
		"BPIRA0311_F03",
		"BPIRA0312_F03",
		"BPIRA0314_F03",
		"BTI0301_F03",
		"BTI0319_F03",
		"BTI0320_F03",
		"BTI0321_F03",
		"BTIR0303_F03",
		"BTIR0305_F03",
		"BTIR0306_F03",
		"BTIR0307_F03",
		"BTIR0308_F03",
		"BTIR0309_F03",
		"BTIR0310_F03",
		"BTIR0311_F03",
		"BTIR0312_F03",
		"BTIR0313_F03",
		"BTIR0314_F03",
		"BTIR0315_F03",
		"BTIR0316_F03",
		"FEED_SK04_F03",
		"SETPOINT04_F03",
		"BFIC_3002_F03_MV")

	val schemaString = "time,AFIC_3001_F03_MV,AFIC_3002_F03_MV,AFIC_3003_F03_MV,AFIC_3005_F03_MV,AFIC_3006_F03_MV,AFIC_3007_F03_MV,AFIC_3020_F03_MV,AFIC_3021_F03_MV,AFIC0302_F03,AFIC0304_F03,AFIC0305_F03,AFIQ0306_F03,AMIC_C301_F03_MV,AMIC_C302_F03_MV,AMIC_L303_F03_MV,AMII_C301_F03,AMII_C302_F03,AMIIL303_F03,APIA0303_F03,APIA0304_F03,APIA0307_F03,APIA0308_F03,APIR0305_F03,APIR0321_F03,APIRA0311_F03,APIRA0312_F03,APIRA0314_F03,ATI0301_F03,ATI0319_F03,ATI0320_F03,ATI0321_F03,ATIR0302_F03,ATIR0303_F03,ATIR0304_F03,ATIR0305_F03,ATIR0306_F03,ATIR0307_F03,ATIR0308_F03,ATIR0309_F03,ATIR0310_F03,ATIR0311_F03,ATIR0312_F03,ATIR0313_F03,ATIR0314_F03,ATIR0315_F03,ATIR0316_F03,FEED_SK03_F03,PIA0302_F03,TI0318_F03,SETPOINT03_F03,BFIC_3021_F03_MV,BFIC0304_F03,BMII_C301_F03,BFIC0305_F03,BMIC_C301_F03_MV,BFIC_3020_F03_MV,BFIC_3005_F03_MV,BFIC_3001_F03_MV,BFIC0302_F03,BFIC_3003_F03_MV,BFIC_3007_F03_MV,BFIQ0306_F03,BMIC_L303_F03_MV,BPIA0303_F03,BMII_C302_F03,BTIR0302_F03,BPIA0308_F03,BFIC_3006_F03_MV,BTIR0304_F03,BMIC_C302_F03_MV,BMIIL303_F03,BPIA0304_F03,BPIA0307_F03,BPIR0305_F03,BPIR0321_F03,BPIRA0311_F03,BPIRA0312_F03,BPIRA0314_F03,BTI0301_F03,BTI0319_F03,BTI0320_F03,BTI0321_F03,BTIR0303_F03,BTIR0305_F03,BTIR0306_F03,BTIR0307_F03,BTIR0308_F03,BTIR0309_F03,BTIR0310_F03,BTIR0311_F03,BTIR0312_F03,BTIR0313_F03,BTIR0314_F03,BTIR0315_F03,BTIR0316_F03,FEED_SK04_F03,SETPOINT04_F03,BFIC_3002_F03_MV"
}


