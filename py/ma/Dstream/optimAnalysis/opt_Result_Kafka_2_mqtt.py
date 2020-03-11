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

            for item in ResultList:
                predictResult = {"predictResult": item}
                print(json.dumps(predictResult))
                self.on_publish(conf.EMQ_TOPIC_OPT, json.dumps(predictResult), 1)
                time.sleep(2)


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
                            vResultItemDict["optCol"].append({
                                "enCode": oClmnName,
                                "cnCode": v["cnCode"],
                                "unit": v["enUnit"],
                                "resultValue": "%.4f" % (float(oRow.get(oClmnName))),
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

                # print("2222222222222...{}".format(json.dumps(vResultItemDict)))

                # 插入, 结果集列表.
                if vResultItemDict['time']:
                    vResultList.append(vResultItemDict)
            # break

        # print("2222222222222...vResultList_len={}".format(len(vResultList)))
        return vResultList


if __name__ == '__main__':
    result = opt_Result_Kafka_2_mqtt()
    result.on_mqtt_connect()
    result.kafa_2_mqtt()


