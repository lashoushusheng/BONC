# !/usr/bin/python
# -*- coding: utf-8 -*-
from kafka import KafkaConsumer

from CConfig import conf
from DModel.Mysql_MA_Result import Mysql_MA_Result
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
        resultList = []
        for item in row.split("**"):
            # print(item)
            itemDict = {}
            itemList = item.split("##")
            modelName = itemList[0]
            data = ast.literal_eval(itemList[1])
            modelParams = ast.literal_eval(itemList[2])
            # self.result_2_mysql(modelName, data, modelParams)

            itemDict["modelName"] = modelName
            itemDict["data"] = data
            itemDict["modelParams"] = modelParams
            resultList.append(itemDict)
        return resultList

    def result_2_mysql(self, modelName, data, modelParams):
        """
        function: predict result insert into mysql;
        :param modelName:
        :param data:
        :param modelParams:
        :return:
        """
        optColid = 0
        if modelParams:
            print(modelParams[0]['data'][0]['enCode'])
            if modelParams[0]['data'][0]['enCode'].find("B") >= 0:
                optColid = 1
            else:
                optColid = 2

        for item in data:
            Mysql_MA_Result.soft_result_insert_2mysql(modelName, optColid, item['time'], item['prediction'])


if __name__ == '__main__':
    result = soft_Result_Kafka_2_mqtt()
    result.on_mqtt_connect()
    result.kafa_2_mqtt()


