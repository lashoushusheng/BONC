package rtcompute.DStruct

/*
	[DataPoint].项.
 */
case class Item_MaTrain(

    var trainId:Int,       				    // 主键ID.
    var modelType:String = "",        // 模型类型.
    var modelName:String = "",        // 模型名称.
    var modelParams4ml:String = "",   // 模型参数json字符串.

		var dsId:Int,               // 数据源ID.
    var dsDir:String = "",      // 数据源目录.
    var dsFile:String = "",     // 数据文件名称.

		var trainDir:String = "",   // 训练结果目录.
		var trainState:Int          // 训练状态，0未开始，1进行中，2已完成.
)
