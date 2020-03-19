# !/usr/bin/python
# -*- coding: utf-8 -*-
from kafka import KafkaConsumer

from CConfig import conf
import paho.mqtt.client as mqtt
import ast
import pandas as pd
import numpy as np
import time
import json

from DPublic.MyLog import MyLog

logFname = '{}/rtc_kafka_2db.log'.format(conf.LOG_PATH)
mylog = MyLog(logFname, level=conf.LOG_LEVEL).logger


class opt_Result_Kafka_2_mqtt(object):
    """
    kafka to mqtt
    """
    def __init__(self):
        # kafka parameter
        self.kafkaConsumer = KafkaConsumer(
            conf.KAFKA_OPT_RESULT_TOPIC, bootstrap_servers=[conf.KAFKA_URL]
        )
        # mqtt init
        self.mqttClient = mqtt.Client()

    # 连接MQTT服务器
    def on_mqtt_connect(self):
        self.mqttClient.connect(conf.EMQ_HOST, conf.EMQ_PORT, conf.EMQ_PRODUCER_KEEPALIVE)
        self.mqttClient.loop_start()

    # publish 消息
    def on_publish(self, topic, payload, qos):
        self.mqttClient.publish(topic, payload, qos)

    # 消息处理函数
    def on_message_come(self, lient, userdata, msg):
        print(msg.topic + " " + ":" + str(msg.payload))

    # subscribe 消息
    def on_subscribe(self):
        self.mqttClient.subscribe("/server", 1)
        self.mqttClient.on_message = self.on_message_come  # 消息到来处理函数

    def kafa_2_mqtt(self):
        for msg in self.kafkaConsumer:
            vKey = None
            vValue = bytes.decode(msg.value)
            ResultList = self.opt_compute_fetch_predict_result(vValue)

            # 一条一条发送
            # for item in ResultList:
            #     predictResult = {"predictResult": item}
            #     print(json.dumps(predictResult))
            #     self.on_publish(conf.EMQ_TOPIC_OPT, json.dumps(predictResult), 1)
            #     time.sleep(2)

            # 批量发送
            predictResult = {"predictResult": ResultList}
            self.on_publish(conf.EMQ_TOPIC_OPT, json.dumps(predictResult), 1)

    def opt_compute_fetch_predict_result(self, row):
        """
            预测结果、输入结果，规整格式，返回给前端.
        """
        if len(row) == 0:
            return

        value = row.split("##")

        data = value[0]
        paramOriJson = value[1]

        dataList = ast.literal_eval(data)
        df = pd.DataFrame(dataList)

        # 获取列信息
        columns = list(df)

        # 过滤出src数据列名
        srcColumns = list(filter(lambda n: n[-2:] == "_o", columns))
        # 结果datafream列名
        resColumns = [i for i in columns if i not in srcColumns]
        # 结果datafream
        dfOutput = df[resColumns]
        # sort by time asc
        dfOutput.sort_values(by=['time'], ascending=True, inplace=True)
        # print(dfOutput)
        # print("*" * 100)

        srcColumns.append('time')
        # # 过滤出原始数据
        dfInput = df[srcColumns]

        # 去掉列名后缀
        srcColumnsnew = list(map(lambda x: x[:-2] if x[-2:] == "_o" else x, srcColumns))
        #
        # # 去掉原始数据列名后缀
        dfInput.columns = srcColumnsnew
        # print(dfInput)
        # print("*" * 100)

        # print("paramOriJson...{}".format(paramOriJson))
        oriParamDict = json.loads(paramOriJson)

        # merge，结果、输入文件.
        vResultList = []
        # 逐行处理.
        for index, oRow in dfOutput.iterrows():
            # 取结果文件[time]关键字.
            oTime = oRow['time']
            # print(oRow)

            # 按time索引，过滤匹配input记录.
            iRow = dfInput[dfInput['time'] == oTime]

            if len(iRow) > 0:
                iRow = iRow.iloc[0]  # 只取第1行.
                vResultItemDict = {
                    "time": None,
                    "gw_id": None,
                    "optCol": [],
                    "paramCol": [],
                }
                # 逐列计算.
                for oClmnName in dfOutput.columns:
                    if oClmnName == "time":  # 时间参数.
                        vResultItemDict["time"] = {
                            "resultValue": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(oRow.get(oClmnName)))),
                            "inValue": oRow.get(oClmnName),
                        }
                    elif oClmnName == "gw_id":  # 工况变量.
                        vResultItemDict["gw_id"] = {
                            "resultValue": int(oRow.get(oClmnName)),
                        }
                    elif oClmnName == "op":  # .
                        vResultItemDict["op"] = {
                            "resultValue": int(oRow.get(oClmnName)),
                        }
                    elif oClmnName in ["CZ3_OP1", "CZ3_OP2", "CZ3_OP3"]:
                        v = oriParamDict.get(oClmnName, None)
                        if v is None:
                            continue
                        # 目标列，插入列表.
                        if v["belongCate"] == "optCol":
                            resultValue = "%.4f" % (float(oRow.get(oClmnName)))
                            if float(resultValue) < 0:
                                resultValue = "-"

                            vResultItemDict["optCol"].append({
                                "enCode": oClmnName,
                                "cnCode": v["cnCode"],
                                "unit": v["enUnit"],
                                "resultValue": resultValue,
                            })

                    else:
                        v = oriParamDict.get(oClmnName, None)
                        if v is None:
                            continue

                        # 参数列，插入列表.
                        if v["belongCate"].find("observedCol") >= 0:
                            vResultItemDict["paramCol"].append({
                                "enCode": oClmnName,
                                "cnCode": v["cnCode"],
                                "unit": v["enUnit"],
                                "resultValue": "%.4f" % (float(oRow.get(oClmnName))),
                                "inputValue": "%.4f" % (float(iRow.get(oClmnName))),
                                "diffValue": "%.4f" % (float(oRow.get(oClmnName)) - float(iRow.get(oClmnName)))
                            })
                        else:
                            vResultItemDict["paramCol"].append({
                                "enCode": oClmnName,
                                "cnCode": v["cnCode"],
                                "unit": v["enUnit"],
                                "resultValue": "-",
                                "inputValue": "%.4f" % (float(iRow.get(oClmnName))),
                                "diffValue": "-"
                            })


                # print("2222222222222...{}".format(json.dumps(vResultItemDict)))

                # 插入, 结果集列表.
                if vResultItemDict['time']:
                    vResultList.append(vResultItemDict)
            # break

        # print("2222222222222...vResultList_len={}".format(len(vResultList)))
        return vResultList


if __name__ == '__main__':
    row = """[{"AFIC_3001_F03_MV_o":100.0,"AFIC0302_F03_o":4.747253,"AFIC_3003_F03_MV_o":43.003659999999996,"APIA0303_F03_o":59.78021999999999,"ATIR0302_F03_o":52.9304,"PIA0302_F03_o":416.7033,"ATIR0304_F03_o":49.30403,"APIA0304_F03_o":163.2479,"APIR0305_F03_o":36.263740000000006,"ATI0301_F03_o":252.0146,"ATIR0303_F03_o":53.150180000000006,"ATIR0305_F03_o":834.2857,"ATIR0306_F03_o":115.4579,"FEED_SK03_F03_o":7.1999509999999995,"SETPOINT03_F03_o":7.2,"AFIC_3002_F03_MV_o":60.83028,"gw_id":164,"AFIC_3001_F03_MV":100.0,"AFIC0302_F03":3.4779,"AFIC_3003_F03_MV":34.99,"APIA0303_F03":103.85,"ATIR0302_F03":56.12,"PIA0302_F03":409.7,"ATIR0304_F03":54.5,"APIA0304_F03":156.83,"APIR0305_F03":29.41,"ATI0301_F03":253.19,"ATIR0303_F03":72.41,"ATIR0305_F03":455.76,"ATIR0306_F03":155.38,"FEED_SK03_F03":3.2473,"SETPOINT03_F03":5.4,"AFIC_3002_F03_MV":56.47,"CZ3_OP1":-1,"CZ3_OP2":1.016,"CZ3_OP3":7.77,"op":0.0,"time":1578100146}, {"AFIC_3001_F03_MV_o":100.0,"AFIC0302_F03_o":4.561661,"AFIC_3003_F03_MV_o":43.003659999999996,"APIA0303_F03_o":91.72161,"ATIR0302_F03_o":52.71062,"PIA0302_F03_o":483.8095,"ATIR0304_F03_o":48.24176,"APIA0304_F03_o":158.8523,"APIR0305_F03_o":32.60073,"ATI0301_F03_o":243.0037,"ATIR0303_F03_o":56.263740000000006,"ATIR0305_F03_o":850.9889999999999,"ATIR0306_F03_o":180.5128,"FEED_SK03_F03_o":7.185247,"SETPOINT03_F03_o":7.2,"AFIC_3002_F03_MV_o":66.95971,"gw_id":27,"AFIC_3001_F03_MV":76.67,"AFIC0302_F03":3.6049,"AFIC_3003_F03_MV":32.99,"APIA0303_F03":163.22,"ATIR0302_F03":58.3,"PIA0302_F03":531.89,"ATIR0304_F03":56.53,"APIA0304_F03":169.96,"APIR0305_F03":31.16,"ATI0301_F03":246.67,"ATIR0303_F03":73.96,"ATIR0305_F03":583.49,"ATIR0306_F03":196.6,"FEED_SK03_F03":4.2633,"SETPOINT03_F03":5.751,"AFIC_3002_F03_MV":56.7,"CZ3_OP1":0.639,"CZ3_OP2":0.96,"CZ3_OP3":9.488,"op":0.0,"time":1578117420}, {"AFIC_3001_F03_MV_o":100.0,"AFIC0302_F03_o":4.6129430000000005,"AFIC_3003_F03_MV_o":43.003659999999996,"APIA0303_F03_o":80.7326,"ATIR0302_F03_o":52.27106,"PIA0302_F03_o":460.3663,"ATIR0304_F03_o":47.91209,"APIA0304_F03_o":153.2357,"APIR0305_F03_o":32.60073,"ATI0301_F03_o":243.4432,"ATIR0303_F03_o":56.263740000000006,"ATIR0305_F03_o":850.9889999999999,"ATIR0306_F03_o":188.3272,"FEED_SK03_F03_o":7.191926,"SETPOINT03_F03_o":7.2,"AFIC_3002_F03_MV_o":62.539680000000004,"gw_id":68,"AFIC_3001_F03_MV":100.0,"AFIC0302_F03":3.5371,"AFIC_3003_F03_MV":34.99,"APIA0303_F03":96.35,"ATIR0302_F03":56.14,"PIA0302_F03":402.45,"ATIR0304_F03":53.75,"APIA0304_F03":158.79,"APIR0305_F03":29.51,"ATI0301_F03":260.64,"ATIR0303_F03":71.25,"ATIR0305_F03":457.41,"ATIR0306_F03":154.19,"FEED_SK03_F03":4.0029,"SETPOINT03_F03":5.4,"AFIC_3002_F03_MV":57.35,"CZ3_OP1":0.625,"CZ3_OP2":1.055,"CZ3_OP3":7.65,"op":0.0,"time":1578117240}, {"AFIC_3001_F03_MV_o":100.0,"AFIC0302_F03_o":4.637362,"AFIC_3003_F03_MV_o":43.003659999999996,"APIA0303_F03_o":66.08059,"ATIR0302_F03_o":52.16117,"PIA0302_F03_o":414.7985,"ATIR0304_F03_o":47.8022,"APIA0304_F03_o":150.5495,"APIR0305_F03_o":31.746029999999998,"ATI0301_F03_o":243.956,"ATIR0303_F03_o":56.263740000000006,"ATIR0305_F03_o":850.9889999999999,"ATIR0306_F03_o":193.602,"FEED_SK03_F03_o":7.224227000000001,"SETPOINT03_F03_o":7.2,"AFIC_3002_F03_MV_o":61.75824,"gw_id":27,"AFIC_3001_F03_MV":76.67,"AFIC0302_F03":3.6049,"AFIC_3003_F03_MV":32.99,"APIA0303_F03":163.22,"ATIR0302_F03":58.3,"PIA0302_F03":531.89,"ATIR0304_F03":56.53,"APIA0304_F03":169.96,"APIR0305_F03":31.16,"ATI0301_F03":246.67,"ATIR0303_F03":73.96,"ATIR0305_F03":583.49,"ATIR0306_F03":196.6,"FEED_SK03_F03":4.2633,"SETPOINT03_F03":5.751,"AFIC_3002_F03_MV":56.7,"CZ3_OP1":0.639,"CZ3_OP2":0.96,"CZ3_OP3":9.488,"op":0.0,"time":1578117060}, {"AFIC_3001_F03_MV_o":100.0,"AFIC0302_F03_o":4.6520150000000005,"AFIC_3003_F03_MV_o":43.003659999999996,"APIA0303_F03_o":65.78754,"ATIR0302_F03_o":51.97802,"PIA0302_F03_o":412.6007,"ATIR0304_F03_o":47.58242,"APIA0304_F03_o":149.2063,"APIR0305_F03_o":31.746029999999998,"ATI0301_F03_o":244.3223,"ATIR0303_F03_o":56.373630000000006,"ATIR0305_F03_o":850.1099,"ATIR0306_F03_o":198.0952,"FEED_SK03_F03_o":7.176649,"SETPOINT03_F03_o":7.2,"AFIC_3002_F03_MV_o":62.588519999999995,"gw_id":173,"AFIC_3001_F03_MV":78.29,"AFIC0302_F03":2.2414,"AFIC_3003_F03_MV":23.1,"APIA0303_F03":116.95,"ATIR0302_F03":54.08,"PIA0302_F03":418.05,"ATIR0304_F03":51.01,"APIA0304_F03":124.59,"APIR0305_F03":19.07,"ATI0301_F03":218.31,"ATIR0303_F03":79.53,"ATIR0305_F03":577.74,"ATIR0306_F03":365.09,"FEED_SK03_F03":2.3857,"SETPOINT03_F03":4.1147,"AFIC_3002_F03_MV":39.24,"CZ3_OP1":0.706,"CZ3_OP2":0.9,"CZ3_OP3":22.96,"op":0.0,"time":1578116880}, {"AFIC_3001_F03_MV_o":100.0,"AFIC0302_F03_o":4.742369,"AFIC_3003_F03_MV_o":43.003659999999996,"APIA0303_F03_o":57.4359,"ATIR0302_F03_o":53.003659999999996,"PIA0302_F03_o":400.7326,"ATIR0304_F03_o":49.48718,"APIA0304_F03_o":163.0037,"APIR0305_F03_o":36.38584,"ATI0301_F03_o":252.38099999999997,"ATIR0303_F03_o":53.333330000000004,"ATIR0305_F03_o":831.9414,"ATIR0306_F03_o":116.2393,"FEED_SK03_F03_o":7.172871000000001,"SETPOINT03_F03_o":7.2,"AFIC_3002_F03_MV_o":59.53601999999999,"gw_id":27,"AFIC_3001_F03_MV":76.67,"AFIC0302_F03":3.6049,"AFIC_3003_F03_MV":32.99,"APIA0303_F03":163.22,"ATIR0302_F03":58.3,"PIA0302_F03":531.89,"ATIR0304_F03":56.53,"APIA0304_F03":169.96,"APIR0305_F03":31.16,"ATI0301_F03":246.67,"ATIR0303_F03":73.96,"ATIR0305_F03":583.49,"ATIR0306_F03":196.6,"FEED_SK03_F03":4.2633,"SETPOINT03_F03":5.751,"AFIC_3002_F03_MV":56.7,"CZ3_OP1":0.639,"CZ3_OP2":0.96,"CZ3_OP3":9.488,"op":0.0,"time":1578100211}]##{"AFIC_3021_F03_MV": {"cnCode": "2#\u70892#\u7f57\u8328\u98ce\u673a\u51fa\u53e3\u98ce\u91cf\u8c03\u9600", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "AFIC0304_F03": {"cnCode": "\u4e00\u6b21\u98ce\u673a\u6d41\u91cf", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "AMII_C301_F03": {"cnCode": "1#\u7a7a\u6c14\u98ce\u673a\u7535\u6d41", "belongCate": "observedCol/decisionCol", "enUnit": "A"}, "AFIC0305_F03": {"cnCode": "\u4e8c\u6b21\u98ce\u673a\u6d41\u91cf", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "AMIC_C301_F03_MV": {"cnCode": "1#\u7a7a\u6c14\u98ce\u673a\u8f6c\u901f\u63a7\u5236", "belongCate": "observedCol/decisionCol", "enUnit": "rpm"}, "AFIC_3020_F03_MV": {"cnCode": "2#\u70891#\u7f57\u8328\u98ce\u673a\u51fa\u53e3\u98ce\u91cf\u8c03\u9600", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "AFIC_3005_F03_MV": {"cnCode": "1#\u7f57\u8328\u98ce\u673a\u51fa\u98ce\u91cf\u8c03", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "AFIC_3001_F03_MV": {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u8c03\u8282", "belongCate": "observedCol/decisionCol", "enUnit": "t/h"}, "AFIC0302_F03": {"cnCode": "AHF\u6362\u70ed\u5668\u8fdb\u53e3AHF\u6d41\u91cf", "belongCate": "observedCol/decisionCol", "enUnit": "t/h"}, "AFIC_3003_F03_MV": {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u538b\u8c03", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "AFIC_3007_F03_MV": {"cnCode": "\u8fdb\u4e0b\u6599\u65cb\u8f6c\u9600\u51b7\u5374\u6c34\u8c03", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "AFIQ0306_F03": {"cnCode": "\u8fdb\u4e0b\u6599\u65cb\u8f6c\u9600\u51b7\u5374\u6c34F", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "AMIC_L303_F03_MV": {"cnCode": "\u6c1f\u5316\u94dd\u4e0b\u6599\u5668\u8f6c\u901f\u8c03\u8282", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "APIA0303_F03": {"cnCode": "AHF\u6362\u70ed\u5668\u8fdb\u53e3\u84b8\u6c7d\u538b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "AMII_C302_F03": {"cnCode": "2#\u7a7a\u6c14\u98ce\u673a\u7535\u6d41\u6307\u793a", "belongCate": "observedCol/decisionCol", "enUnit": "A"}, "ATIR0302_F03": {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "PIA0302_F03": {"cnCode": "\u84b8\u6c7d\u51cf\u538b\u9600\u540e\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "APIA0308_F03": {"cnCode": "2#\u7a7a\u6c14\u98ce\u673a\u51fa\u53e3\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "AFIC_3006_F03_MV": {"cnCode": "2#\u7f57\u8328\u98ce\u673a\u51fa\u98ce\u91cf\u8c03", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "ATIR0304_F03": {"cnCode": "AHF\u6362\u70ed\u5668\u5e95\u90e8\u9178\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "AMIC_C302_F03_MV": {"cnCode": "2#\u7a7a\u6c14\u98ce\u673a\u8f6c\u901f\u63a7\u5236", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "AMIIL303_F03": {"cnCode": "\u6c1f\u5316\u94dd\u4e0b\u6599\u56de\u8f6c\u9600\u7535\u6d41", "belongCate": "observedCol/decisionCol", "enUnit": "A"}, "APIA0304_F03": {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "APIA0307_F03": {"cnCode": "1#\u7a7a\u6c14\u98ce\u673a\u51fa\u53e3\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "APIR0305_F03": {"cnCode": "\u6df7\u5408\u4e09\u901a\u8fdb\u53e3HF\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "APIR0321_F03": {"cnCode": "2\u7ea7\u9664\u5c18\u5668\u8fdb\u53e3\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "APIRA0311_F03": {"cnCode": "\u786b\u5316\u5e8a\u5e95\u90e8\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "APIRA0312_F03": {"cnCode": "\u786b\u5316\u5e8a\u4e2d\u90e8\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "APIRA0314_F03": {"cnCode": "\u4e00\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u8fdb\u53e3\u538b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "ATI0301_F03": {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATI0319_F03": {"cnCode": "\u4e0b\u6599\u56de\u8f6c\u9600\u51b7\u5374\u56de\u6c34\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATI0320_F03": {"cnCode": "\u6c1f\u5316\u94dd\u8fdb\u51b7\u5374\u7089\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATI0321_F03": {"cnCode": "\u6c1f\u5316\u94dd\u51fa\u51b7\u5374\u7089\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0303_F03": {"cnCode": "\u6df7\u5408\u4e09\u901a\u8fdb\u53e3HF\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0305_F03": {"cnCode": "\u81a8\u80c0\u5f2f\u5934\u70ed\u6c14\u4f53\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0306_F03": {"cnCode": "\u6df7\u5408\u4e09\u901a\u6df7\u5408\u6c14\u4f53\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0307_F03": {"cnCode": "\u786b\u5316\u5e8a\u4e0b\u90e8\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0308_F03": {"cnCode": "\u786b\u5316\u5e8a\u4e0a\u90e8\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0309_F03": {"cnCode": "\u4e00\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u51fa\u6c14\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0310_F03": {"cnCode": "\u4e8c\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u4e0b\u53e3\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0311_F03": {"cnCode": "\u4e09\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u51fa\u6c14\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0316_F03": {"cnCode": "2\u7ea7\u9664\u5c18\u5668\u4e0b\u53e3\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0313_F03": {"cnCode": "\u56db\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u51fa\u53e3\u6c14", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "ATIR0314_F03": {"cnCode": "\u56db\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u4e0b\u53e3\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0315_F03": {"cnCode": "2\u7ea7\u9664\u5c18\u5668\u51fa\u53e3\u6c14\u4f53\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "ATIR0312_F03": {"cnCode": "\u4e09\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u4e0b\u53e3\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "FEED_SK03_F03": {"cnCode": "\u6d41\u91cf\u5b9e\u9645\u503c", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "TI0318_F03": {"cnCode": "\u51b7\u5374\u6c34\u4e3b\u7ba1\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "SETPOINT03_F03": {"cnCode": "\u6d41\u91cf\u8bbe\u5b9a", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "AFIC_3002_F03_MV": {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668AHF\u8c03\u8282\u8fdb", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "CZ3_OP1": {"cnCode": "AHF\u5b9e\u9645\u5355\u8017", "belongCate": "optCol", "enUnit": "", "maxvalue": "nan", "minvalue": "nan"}, "CZ3_OP2": {"cnCode": "\u6c22\u94dd\u5b9e\u9645\u5355\u8017", "belongCate": "optCol", "enUnit": "", "maxvalue": "nan", "minvalue": "nan"}, "CZ3_OP3": {"cnCode": "\u5929\u7136\u6c14\u5b9e\u9645\u5355\u8017", "belongCate": "optCol", "enUnit": "", "maxvalue": "nan", "minvalue": "nan"}}"""
    result = opt_Result_Kafka_2_mqtt()
    # result.on_mqtt_connect()
    # result.kafa_2_mqtt()
    ResultList = result.opt_compute_fetch_predict_result(row)
    predictResult = {"predictResult": ResultList}
    print(json.dumps(predictResult))


