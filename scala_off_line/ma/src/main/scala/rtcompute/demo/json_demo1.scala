//package rtcompute.demo
//
//import com.alibaba.fastjson.{JSON, JSONObject}
//
//import scala.collection.mutable.ArrayBuffer
//import scala.collection.mutable
//
//
//object json_demo1 {
//
//	var demoResultHashMap:mutable.HashMap[String, DemoNodeItem] =
//		new mutable.HashMap[String, DemoNodeItem]()
//
//	case class DemoNodeItem (
//        var nodeId:String = "",             // 结点Id.
//        var nodeLabel:String = "",          // 结点Label.
//        var datapointId:String = "",        // 结点Explain.
//        var constantValue:String = "",      // 常量.
//
//		// 来源结点Id列表.
//		var sourceIdList:ArrayBuffer[String] = new ArrayBuffer[String]
//    )
//
//
//	val formularJson = "{\"flowId\": \"60002\", \"flowName\": \"\\u6d4b\\u8bd52\", \"timeWindow\": 60, \"timeInterval\": 60, \"formulaDesc\": \"($6010+$6011)/$6012*1000\", \"allDescribeData\": [{\"nodeInfo\": {\"actName\": \"Multiply\", \"nodeId\": \"700047\"}, \"sourceLocation\": [{\"sourceId\": \"700044\"}, {\"sourceId\": \"700046\"}], \"destLocation\": [{\"destNodeId\": \"700049\"}], \"nodeParameter\": {\"nodeLabel\": \"Multiply\", \"nodeExplain\": \"Multiply700047\", \"levelNo\": 4}, \"subNode\": [{\"nodeInfo\": {\"actName\": \"Division\", \"nodeId\": \"700044\"}, \"sourceLocation\": [{\"sourceId\": \"700041\"}, {\"sourceId\": \"700043\"}], \"destLocation\": [{\"destNodeId\": \"700047\"}], \"nodeParameter\": {\"nodeLabel\": \"Division\", \"nodeExplain\": \"Division700044\", \"levelNo\": 3}, \"subNode\": [{\"nodeInfo\": {\"actName\": \"Sum\", \"nodeId\": \"700041\"}, \"sourceLocation\": [{\"sourceId\": \"700039\"}, {\"sourceId\": \"700040\"}], \"destLocation\": [{\"destNodeId\": \"700044\"}], \"nodeParameter\": {\"nodeLabel\": \"Sum\", \"nodeExplain\": \"Sum700041\", \"levelNo\": 2}, \"subNode\": [{\"nodeInfo\": {\"actName\": \"datapoint\", \"nodeId\": \"700039\"}, \"sourceLocation\": [], \"destLocation\": [{\"destNodeId\": \"700041\"}], \"nodeParameter\": {\"nodeLabel\": \"\\u7269\\u7406\\u70b9_6010\", \"nodeExplain\": \"Sensor_6010\", \"datapointId\": \"6010\", \"datapointName\": \"datapoint_6010\", \"sensorPosition\": 0, \"levelNo\": 1}, \"subNode\": []}, {\"nodeInfo\": {\"actName\": \"datapoint\", \"nodeId\": \"700040\"}, \"sourceLocation\": [], \"destLocation\": [{\"destNodeId\": \"700041\"}], \"nodeParameter\": {\"nodeLabel\": \"\\u7269\\u7406\\u70b9_6011\", \"nodeExplain\": \"Sensor_6011\", \"datapointId\": \"6011\", \"datapointName\": \"datapoint_6011\", \"sensorPosition\": 1, \"levelNo\": 1}, \"subNode\": []}]}, {\"nodeInfo\": {\"actName\": \"datapoint\", \"nodeId\": \"700043\"}, \"sourceLocation\": [], \"destLocation\": [{\"destNodeId\": \"700044\"}], \"nodeParameter\": {\"nodeLabel\": \"\\u7269\\u7406\\u70b9_6012\", \"nodeExplain\": \"Sensor_6012\", \"datapointId\": \"6012\", \"datapointName\": \"datapoint_6012\", \"sensorPosition\": 1, \"levelNo\": 1}, \"subNode\": []}]}, {\"nodeInfo\": {\"actName\": \"Constant\", \"nodeId\": \"700046\"}, \"sourceLocation\": [], \"destLocation\": [{\"destNodeId\": \"700047\"}], \"nodeParameter\": {\"nodeLabel\": \"Constant\", \"nodeExplain\": \"Constant700046\", \"constantValue\": \"1000\", \"levelNo\": 1}, \"subNode\": []}]}]}"
//
//	def main(args: Array[String]): Unit = {
//		println(formularJson)
//
//		val vObj = JSON.parseObject(formularJson)
//		println(vObj)
//
//		val vJsonOBJ = vObj.getJSONArray("allDescribeData").getJSONObject(0)
//		println(vJsonOBJ)
//
//		this.parse_item(vJsonOBJ)
//
//	}
//
//
//	def parse_item(jsonOBJ:JSONObject): Unit ={
//
//		val vItem = DemoNodeItem()
//
//		var vObj = jsonOBJ.getJSONObject("nodeInfo")
//		if( vObj != null ){
//			vItem.nodeId = vObj.getString("nodeId")
//		}
//
//		// [取nodeParameter].信息.
//		vObj = jsonOBJ.getJSONObject("nodeParameter")
//
//		if( vObj != null ){
//			vItem.nodeLabel = vObj.getString("nodeLabel")
//			vItem.datapointId = vObj.getString("datapointId")        // 物理点ID.
//			vItem.constantValue = vObj.getString("constantValue")    // 常量.
//		}
//
//		// [取sourceLocation].sourceId.
//		var vArray = jsonOBJ.getJSONArray("sourceLocation")
//		if( vArray != null ){
//			for(i <- 0 until vArray.size)
//				vItem.sourceIdList.append(
//					vArray.getJSONObject(i).getString("sourceId")
//				)
//		}
//
//
//		// 打印.调试.
//		println(s"$vItem.toString")
//
//		// [递归]，下一级.
//		vArray = jsonOBJ.getJSONArray("subNode")
//		if( vArray != null ){
//			for(i <- 0 until vArray.size)
//				parse_item(vArray.getJSONObject(i))
//		}
//	}
//
//}
