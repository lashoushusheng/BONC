package rtcompute.DStruct

/*
	[DataPoint].项.
 */
case class Item_MaPredict(

    var predId:Int,       // 主键ID.
    var modelType:String = "",  // 模型类型.
    var modelName:String = "",  // 模型名称.

		var trainId:Int,            // 训练ID.
    var trainDir:String = "",   // 训练目录.

		var paramOriJson:String = "", // 原始参数
    var modelParams:String = "",

    var dsId:Int,               // 数据源ID.
    var dsDir:String = "",      // 数据源目录.
    var dsFile:String = "",     // 数据文件名称.

    var predictDir:String = "", // 预测目录.
		var predictState:Int        // 预测状态，0未开始，1进行中，2已完成.
)
