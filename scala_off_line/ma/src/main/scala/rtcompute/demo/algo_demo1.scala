package rtcompute.demo

//import com.bonc.interfaceRaw.IBGA_Model
//import com.bonc.utils.df2schemaUtils
import org.apache.spark.sql.SparkSession


object algo_demo1 {

	def main(args: Array[String]): Unit = {
		println("111111111111")

//		val vObj = IBGA_Model.train_task_commit(
//			var1 = "1", var2 = "2", var3 = "3"
//		)

//		val spark=SparkSession.builder().getOrCreate()
		val spark  = SparkSession.builder()
			.master("local[2]")
			.appName("ZxyyRtcCompute")
			.getOrCreate()

		var df1 = spark.read.json("E:\\code\\Athena\\taurus_开发_测试\\项目poc_模型分析16\\name.json")
		println(df1)
		println(df1.show())

//		val vObj = df2schemaUtils.df2Round(
//			df1=df1, "1", 0
//		)
//		println(vObj)
	}

}
