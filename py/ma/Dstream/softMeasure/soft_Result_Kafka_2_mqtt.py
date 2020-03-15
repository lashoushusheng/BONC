# !/usr/bin/python
# -*- coding: utf-8 -*-
from kafka import KafkaConsumer

from CConfig import conf
import paho.mqtt.client as mqtt
import pandas as pd
import time
import json
import ast

from DPublic.MyLog import MyLog

logFname = '{}/rtc_kafka_2db.log'.format(conf.LOG_PATH)
mylog = MyLog(logFname, level=conf.LOG_LEVEL).logger


class soft_Result_Kafka_2_mqtt(object):
    """
    kafka to mqtt
    """
    def __init__(self):
        # kafka parameter
        self.kafkaConsumer = KafkaConsumer(
            conf.KAFKA_SOFT_RESULT_TOPIC, bootstrap_servers=[conf.KAFKA_URL]
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
            resultList = self.fetch_predict_result(vValue)
            predictResult = {"predictResult": resultList}
            print(json.dumps(predictResult))
            self.on_publish(conf.EMQ_TOPIC_SOFT, json.dumps(predictResult), 1)

    def fetch_predict_result(self, row):
        """
        :param row:
        :return:
        """
        # row = """test2##[{"time":"2020-01-04 10:00:00","prediction":33.4370942967495}, {"time":"2020-01-04 10:03:00","prediction":33.4130942967495}, {"time":"2020-01-04 10:06:00","prediction":33.4370942967495}, {"time":"2020-01-04 10:09:00","prediction":33.39102286817807}, {"time":"2020-01-04 10:12:00","prediction":33.37416383138154}, {"time":"2020-01-04 10:15:00","prediction":33.297488236143444}]##[{"enStep": "optCol", "cnStep": "\u4f18\u5316\u76ee\u6807", "data": [{"cnCode": "B(%)", "enCode": "B(%)", "maxvalue": "34.0", "minvalue": "32.6"}]}, {"enStep": "decisionCol", "cnStep": "\u5f3a\u76f8\u5173\u64cd\u4f5c\u53d8\u91cf", "data": [{"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u8c03\u8282", "enCode": "BFIC_3001_F03_MV"}, {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668AHF\u8c03\u8282", "enCode": "BFIC_3002_F03_MV"}, {"cnCode": "1#\u7f57\u8328\u98ce\u673a\u51fa\u98ce\u91cf\u8c03", "enCode": "BFIC_3005_F03_MV"}]}]**test1##[{"time":"2020-01-04 10:00:00","prediction":60.54246067977644}, {"time":"2020-01-04 10:03:00","prediction":60.54246067977644}, {"time":"2020-01-04 10:06:00","prediction":60.53312241848922}, {"time":"2020-01-04 10:09:00","prediction":60.490217090778465}, {"time":"2020-01-04 10:12:00","prediction":60.536688616999186}, {"time":"2020-01-04 10:15:00","prediction":60.61071589332075}]##[{"enStep": "optCol", "cnStep": "\u4f18\u5316\u76ee\u6807", "data": [{"cnCode": "A(%)", "enCode": "A(%)", "maxvalue": "62.0", "minvalue": "59.5"}]}, {"enStep": "decisionCol", "cnStep": "\u5f3a\u76f8\u5173\u64cd\u4f5c\u53d8\u91cf", "data": [{"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u8c03\u8282", "enCode": "BFIC_3001_F03_MV"}, {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668AHF\u8c03\u8282", "enCode": "BFIC_3002_F03_MV"}, {"cnCode": "1#\u7f57\u8328\u98ce\u673a\u51fa\u98ce\u91cf\u8c03", "enCode": "BFIC_3005_F03_MV"}, {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u538b\u8c03", "enCode": "BFIC_3003_F03_MV"}, {"cnCode": "2#\u7f57\u8328\u98ce\u673a\u51fa\u98ce\u91cf\u8c03", "enCode": "BFIC_3006_F03_MV"}, {"cnCode": "2#\u70892#\u7f57\u8328\u98ce\u673a\u51fa\u53e3\u98ce\u91cf\u8c03\u9600", "enCode": "BFIC_3021_F03_MV"}, {"cnCode": "AHF\u6362\u70ed\u5668\u8fdb\u53e3AHF\u6d41\u91cf", "enCode": "BFIC0302_F03"}, {"cnCode": "\u4e8c\u6b21\u98ce\u673a\u6d41\u91cf", "enCode": "BFIC0305_F03"}, {"cnCode": "2#\u7a7a\u6c14\u98ce\u673a\u8f6c\u901f\u63a7\u5236", "enCode": "BMIC_C302_F03_MV"}, {"cnCode": "AHF\u6362\u70ed\u5668\u8fdb\u53e3\u84b8\u6c7d\u538b", "enCode": "BPIA0303_F03"}, {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u538b\u529b", "enCode": "BPIA0304_F03"}, {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u6e29\u5ea6", "enCode": "BTI0301_F03"}, {"cnCode": "\u84b8\u6c7d\u51cf\u538b\u9600\u540e\u538b\u529b", "enCode": "PIA0302_F03"}]}]**test4##[{"time":"2020-01-04 10:00:00","prediction":33.21758333333333}, {"time":"2020-01-04 10:03:00","prediction":33.31400000000001}, {"time":"2020-01-04 10:06:00","prediction":33.21758333333333}, {"time":"2020-01-04 10:09:00","prediction":33.322500000000005}, {"time":"2020-01-04 10:12:00","prediction":33.257749999999994}, {"time":"2020-01-04 10:15:00","prediction":33.226375000000004}]##[{"enStep": "optCol", "cnStep": "\u4f18\u5316\u76ee\u6807", "data": [{"cnCode": "B(%)", "enCode": "B(%)", "maxvalue": "34.0", "minvalue": "32.6"}]}, {"enStep": "decisionCol", "cnStep": "\u5f3a\u76f8\u5173\u64cd\u4f5c\u53d8\u91cf", "data": [{"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u8c03\u8282", "enCode": "BFIC_3001_F03_MV"}, {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668AHF\u8c03\u8282", "enCode": "BFIC_3002_F03_MV"}]}]**test3##[{"time":"2020-01-04 10:00:00","prediction":60.16}, {"time":"2020-01-04 10:03:00","prediction":60.16}, {"time":"2020-01-04 10:06:00","prediction":60.16}, {"time":"2020-01-04 10:09:00","prediction":60.16}, {"time":"2020-01-04 10:12:00","prediction":60.90333333333333}, {"time":"2020-01-04 10:15:00","prediction":60.16}]##[{"enStep": "optCol", "cnStep": "\u4f18\u5316\u76ee\u6807", "data": [{"cnCode": "A(%)", "enCode": "A(%)", "maxvalue": "62.0", "minvalue": "59.5"}]}, {"enStep": "decisionCol", "cnStep": "\u5f3a\u76f8\u5173\u64cd\u4f5c\u53d8\u91cf", "data": [{"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u8c03\u8282", "enCode": "BFIC_3001_F03_MV"}, {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668AHF\u8c03\u8282", "enCode": "BFIC_3002_F03_MV"}, {"cnCode": "2#\u7f57\u8328\u98ce\u673a\u51fa\u98ce\u91cf\u8c03", "enCode": "BFIC_3006_F03_MV"}, {"cnCode": "2#\u70892#\u7f57\u8328\u98ce\u673a\u51fa\u53e3\u98ce\u91cf\u8c03\u9600", "enCode": "BFIC_3021_F03_MV"}, {"cnCode": "AHF\u6362\u70ed\u5668\u8fdb\u53e3AHF\u6d41\u91cf", "enCode": "BFIC0302_F03"}, {"cnCode": "\u4e8c\u6b21\u98ce\u673a\u6d41\u91cf", "enCode": "BFIC0305_F03"}, {"cnCode": "2#\u7a7a\u6c14\u98ce\u673a\u8f6c\u901f\u63a7\u5236", "enCode": "BMIC_C302_F03_MV"}, {"cnCode": "AHF\u6362\u70ed\u5668\u8fdb\u53e3\u84b8\u6c7d\u538b", "enCode": "BPIA0303_F03"}, {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u538b\u529b", "enCode": "BPIA0304_F03"}, {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u6e29\u5ea6", "enCode": "BTI0301_F03"}, {"cnCode": "\u84b8\u6c7d\u51cf\u538b\u9600\u540e\u538b\u529b", "enCode": "PIA0302_F03"}]}]**test5##[{"time":"2020-01-04 10:00:00","prediction":60.54246067977644}, {"time":"2020-01-04 10:03:00","prediction":60.54246067977644}, {"time":"2020-01-04 10:06:00","prediction":60.53312241848922}, {"time":"2020-01-04 10:09:00","prediction":60.490217090778465}, {"time":"2020-01-04 10:12:00","prediction":60.536688616999186}, {"time":"2020-01-04 10:15:00","prediction":60.61071589332075}]##[{"enStep": "optCol", "cnStep": "\u4f18\u5316\u76ee\u6807", "data": [{"cnCode": "A(%)", "enCode": "A(%)", "maxvalue": "62.0", "minvalue": "59.5"}]}, {"enStep": "decisionCol", "cnStep": "\u5f3a\u76f8\u5173\u64cd\u4f5c\u53d8\u91cf", "data": [{"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u8c03\u8282", "enCode": "BFIC_3001_F03_MV"}, {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668AHF\u8c03\u8282", "enCode": "BFIC_3002_F03_MV"}, {"cnCode": "1#\u7f57\u8328\u98ce\u673a\u51fa\u98ce\u91cf\u8c03", "enCode": "BFIC_3005_F03_MV"}, {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u538b\u8c03", "enCode": "BFIC_3003_F03_MV"}, {"cnCode": "2#\u7f57\u8328\u98ce\u673a\u51fa\u98ce\u91cf\u8c03", "enCode": "BFIC_3006_F03_MV"}, {"cnCode": "2#\u70892#\u7f57\u8328\u98ce\u673a\u51fa\u53e3\u98ce\u91cf\u8c03\u9600", "enCode": "BFIC_3021_F03_MV"}, {"cnCode": "AHF\u6362\u70ed\u5668\u8fdb\u53e3AHF\u6d41\u91cf", "enCode": "BFIC0302_F03"}, {"cnCode": "\u4e8c\u6b21\u98ce\u673a\u6d41\u91cf", "enCode": "BFIC0305_F03"}, {"cnCode": "2#\u7a7a\u6c14\u98ce\u673a\u8f6c\u901f\u63a7\u5236", "enCode": "BMIC_C302_F03_MV"}, {"cnCode": "AHF\u6362\u70ed\u5668\u8fdb\u53e3\u84b8\u6c7d\u538b", "enCode": "BPIA0303_F03"}, {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u538b\u529b", "enCode": "BPIA0304_F03"}, {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u6e29\u5ea6", "enCode": "BTI0301_F03"}, {"cnCode": "\u84b8\u6c7d\u51cf\u538b\u9600\u540e\u538b\u529b", "enCode": "PIA0302_F03"}]}]**test6##[{"time":"2020-01-04 10:00:00","prediction":33.21758333333333}, {"time":"2020-01-04 10:03:00","prediction":33.31400000000001}, {"time":"2020-01-04 10:06:00","prediction":33.21758333333333}, {"time":"2020-01-04 10:09:00","prediction":33.322500000000005}, {"time":"2020-01-04 10:12:00","prediction":33.257749999999994}, {"time":"2020-01-04 10:15:00","prediction":33.226375000000004}]##[{"enStep": "optCol", "cnStep": "\u4f18\u5316\u76ee\u6807", "data": [{"cnCode": "B(%)", "enCode": "B(%)", "maxvalue": "34.0", "minvalue": "32.6"}]}, {"enStep": "decisionCol", "cnStep": "\u5f3a\u76f8\u5173\u64cd\u4f5c\u53d8\u91cf", "data": [{"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u8c03\u8282", "enCode": "BFIC_3001_F03_MV"}, {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668AHF\u8c03\u8282", "enCode": "BFIC_3002_F03_MV"}]}]"""
        resultList = []
        for item in row.split("**"):
            itemDict = {}
            itemList = item.split("##")
            itemDict["modelName"] = itemList[0]
            itemDict["data"] = ast.literal_eval(itemList[1])
            itemDict["modelParams"] = ast.literal_eval(itemList[2])
            resultList.append(itemDict)
        return resultList


if __name__ == '__main__':
    result = soft_Result_Kafka_2_mqtt()
    result.on_mqtt_connect()
    result.kafa_2_mqtt()


