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


class soft_Result_Kafka_2_mqtt(object):
    """
    kafka to mqtt
    """
    def __init__(self):
        # kafka parameter
        self.kafkaConsumer = KafkaConsumer(
            conf.KAFKA_GREY_RESULT_TOPIC, bootstrap_servers=[conf.KAFKA_URL]
        )
        # mqtt init
        self.mqttClient = mqtt.Client()
        # 保存实际值
        self.actualDF = pd.DataFrame(columns=['date', 'prediction', 'isFault'])
        # 保存预测值
        self.predictionDF = pd.DataFrame(columns=['date', 'prediction', 'isFault'])
        self.AccuracyList = []
        self.LastTime = ""

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
            # print(vValue)
            resList = ast.literal_eval(vValue)
            Result = {}

            if len(resList) == 18:
                actualValue = resList[0:15]
                predictionValue = resList[15:]
                # print(actualValue)
                # print(predictionValue)
                accuracy = self.mean_accuracy1(actualValue, predictionValue)
                # print("平均预测准确度")
                # print(accuracy)

                Result['actual'] = actualValue
                Result['predict'] = predictionValue
                Result['accuracy'] = accuracy
                print(json.dumps(Result))
                self.on_publish(conf.EMQ_TOPIC, json.dumps(Result), 1)

    def mean_accuracy(self, actualValue, predictionValue):
        """
        功能： 计算平均预测准确度
        param actualValue: 实际值
        param predictionValue: 预测值
        return:
        """
        self.actualDF = self.actualDF.append(actualValue[-1], ignore_index=True)
        # 零点数据清零重新计算
        if actualValue[0]['date'][-8:] == '00:00:00':
            self.actualDF.drop(self.actualDF.index, inplace=True)
            self.predictionDF.drop(self.predictionDF.index, inplace=True)
            self.predictionDF = self.predictionDF.append(predictionValue)

        else:
            if len(self.predictionDF) < len(predictionValue):
                self.predictionDF = self.predictionDF.append(predictionValue)
            else:
                for i in range(len(predictionValue)):
                    self.predictionDF.loc[len(self.predictionDF) - len(predictionValue) + i + 1] =\
                        [predictionValue[i]['date'], predictionValue[i]['prediction'], predictionValue[i]['isFault']]


        # # 逐行处理.
        if self.actualDF.empty:
            return 0

        else:
            AccuracyList = []
            for index, actualRow in self.actualDF.iloc[1:, :].iterrows():
                actualTime = actualRow['date']
                actualValue = actualRow['prediction']
                predictRow = self.predictionDF[self.predictionDF['date'] == actualTime]

                if len(predictRow) <= 0:
                    return 0

                else:
                    predictValue = predictRow['prediction'].reset_index(drop=True)[0]
                    Accuracy = 1 - abs(float(predictValue) - actualValue)/actualValue
                    AccuracyList.append(Accuracy)

            if AccuracyList:
                return np.mean(AccuracyList)
            else:
                return 0

    def mean_accuracy1(self, actualValue, predictionValue):
        """
        功能： 计算平均预测准确度
        param actualValue: 实际值
        param predictionValue: 预测值
        return:
        """
        self.actualDF = self.actualDF.append(actualValue[-1], ignore_index=True)
        if len(self.predictionDF) < len(predictionValue):
            self.predictionDF = self.predictionDF.append(predictionValue)
        else:
            for i in range(len(predictionValue)):
                self.predictionDF.loc[len(self.predictionDF) - len(predictionValue) + i + 1] =\
                    [predictionValue[i]['date'], predictionValue[i]['prediction'], predictionValue[i]['isFault']]

        if actualValue[0]['date'][-8:] == '00:00:00':
            self.AccuracyList.clear()

        self.actualDF.drop(self.actualDF[self.actualDF.date < self.LastTime].index, inplace=True)
        self.predictionDF.drop(self.predictionDF[self.predictionDF.date < self.LastTime].index, inplace=True)

        # # 逐行处理.
        if self.actualDF.empty:
            return 0

        else:
            for index, actualRow in self.actualDF.iterrows():
                actualTime = actualRow['date']
                actualValue = actualRow['prediction']
                predictRow = self.predictionDF[self.predictionDF['date'] == actualTime]

                if len(predictRow) > 0:
                    predictValue = predictRow['prediction'].reset_index(drop=True)[0]
                    Accuracy = 1 - abs(float(predictValue) - actualValue)/actualValue
                    self.AccuracyList.append(Accuracy)
                    self.LastTime = actualTime
        #
        if self.AccuracyList:
            print(len(self.AccuracyList))
            return np.mean(self.AccuracyList)
        else:
            return 0


if __name__ == '__main__':
    result = soft_Result_Kafka_2_mqtt()
    result.on_mqtt_connect()
    result.kafa_2_mqtt()


