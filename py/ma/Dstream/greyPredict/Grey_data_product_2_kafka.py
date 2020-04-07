#!/usr/bin/python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import pandas as pd
import time


from CConfig import conf
from DPublic.MyLog import MyLog

logFname = '{}/Data_product_2_kafka.log'.format(conf.LOG_PATH)
mylog = MyLog(logFname, level=conf.LOG_LEVEL).logger

producer = KafkaProducer(
    value_serializer=lambda v: v.encode('utf-8'),
    bootstrap_servers=[conf.KAFKA_URL]
)


def send_data_2_kafka(df):
    for index, row in df.iterrows():
        # msg = f"{row['time']},{row['T11']}"
        msg = f"{row['time']},{row['TI1103A_values']},{row['TI215_values']},{row['TI284_1_values']}"
        producer.send(conf.KAFKA_GREY_SRC_TOPIC, msg)
        time.sleep(3)


if __name__ == '__main__':
    df = pd.read_csv("/root/works/src/BONC/app16/py/ma/test_demo/date_demo/merge_data_在线数据_sec.csv")
    # df = pd.read_csv("/root/works/idata/ma16_data/origin_data/生产预警分析/predic_data/merge_data_在线数据.csv")
    print(df)
    while True:
        send_data_2_kafka(df)

