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
        msg = f"{row['time']}," \
        f"{row['AFIC_3001_F03_MV']}," \
        f"{row['AFIC_3002_F03_MV']}," \
        f"{row['AFIC_3003_F03_MV']}," \
        f"{row['AFIC_3005_F03_MV']}," \
        f"{row['AFIC_3006_F03_MV']}," \
        f"{row['AFIC_3007_F03_MV']}," \
        f"{row['AFIC_3020_F03_MV']}," \
        f"{row['AFIC_3021_F03_MV']}," \
        f"{row['AFIC0302_F03']}," \
        f"{row['AFIC0304_F03']}," \
        f"{row['AFIC0305_F03']}," \
        f"{row['AFIQ0306_F03']}," \
        f"{row['AMIC_C301_F03_MV']}," \
        f"{row['AMIC_C302_F03_MV']}," \
        f"{row['AMIC_L303_F03_MV']}," \
        f"{row['AMII_C301_F03']}," \
        f"{row['AMII_C302_F03']}," \
        f"{row['AMIIL303_F03']}," \
        f"{row['APIA0303_F03']}," \
        f"{row['APIA0304_F03']}," \
        f"{row['APIA0307_F03']}," \
        f"{row['APIA0308_F03']}," \
        f"{row['APIR0305_F03']}," \
        f"{row['APIR0321_F03']}," \
        f"{row['APIRA0311_F03']}," \
        f"{row['APIRA0312_F03']}," \
        f"{row['APIRA0314_F03']}," \
        f"{row['ATI0301_F03']}," \
        f"{row['ATI0319_F03']}," \
        f"{row['ATI0320_F03']}," \
        f"{row['ATI0321_F03']}," \
        f"{row['ATIR0302_F03']}," \
        f"{row['ATIR0303_F03']}," \
        f"{row['ATIR0304_F03']}," \
        f"{row['ATIR0305_F03']}," \
        f"{row['ATIR0306_F03']}," \
        f"{row['ATIR0307_F03']}," \
        f"{row['ATIR0308_F03']}," \
        f"{row['ATIR0309_F03']}," \
        f"{row['ATIR0310_F03']}," \
        f"{row['ATIR0311_F03']}," \
        f"{row['ATIR0312_F03']}," \
        f"{row['ATIR0313_F03']}," \
        f"{row['ATIR0314_F03']}," \
        f"{row['ATIR0315_F03']}," \
        f"{row['ATIR0316_F03']}," \
        f"{row['FEED_SK03_F03']}," \
        f"{row['PIA0302_F03']}," \
        f"{row['TI0318_F03']}," \
        f"{row['SETPOINT03_F03']}," \
        f"{row['BFIC_3021_F03_MV']}," \
        f"{row['BFIC0304_F03']}," \
        f"{row['BMII_C301_F03']}," \
        f"{row['BFIC0305_F03']}," \
        f"{row['BMIC_C301_F03_MV']}," \
        f"{row['BFIC_3020_F03_MV']}," \
        f"{row['BFIC_3005_F03_MV']}," \
        f"{row['BFIC_3001_F03_MV']}," \
        f"{row['BFIC0302_F03']}," \
        f"{row['BFIC_3003_F03_MV']}," \
        f"{row['BFIC_3007_F03_MV']}," \
        f"{row['BFIQ0306_F03']}," \
        f"{row['BMIC_L303_F03_MV']}," \
        f"{row['BPIA0303_F03']}," \
        f"{row['BMII_C302_F03']}," \
        f"{row['BTIR0302_F03']}," \
        f"{row['BPIA0308_F03']}," \
        f"{row['BFIC_3006_F03_MV']}," \
        f"{row['BTIR0304_F03']}," \
        f"{row['BMIC_C302_F03_MV']}," \
        f"{row['BMIIL303_F03']}," \
        f"{row['BPIA0304_F03']}," \
        f"{row['BPIA0307_F03']}," \
        f"{row['BPIR0305_F03']}," \
        f"{row['BPIR0321_F03']}," \
        f"{row['BPIRA0311_F03']}," \
        f"{row['BPIRA0312_F03']}," \
        f"{row['BPIRA0314_F03']}," \
        f"{row['BTI0301_F03']}," \
        f"{row['BTI0319_F03']}," \
        f"{row['BTI0320_F03']}," \
        f"{row['BTI0321_F03']}," \
        f"{row['BTIR0303_F03']}," \
        f"{row['BTIR0305_F03']}," \
        f"{row['BTIR0306_F03']}," \
        f"{row['BTIR0307_F03']}," \
        f"{row['BTIR0308_F03']}," \
        f"{row['BTIR0309_F03']}," \
        f"{row['BTIR0310_F03']}," \
        f"{row['BTIR0311_F03']}," \
        f"{row['BTIR0312_F03']}," \
        f"{row['BTIR0313_F03']}," \
        f"{row['BTIR0314_F03']}," \
        f"{row['BTIR0315_F03']}," \
        f"{row['BTIR0316_F03']}," \
        f"{row['FEED_SK04_F03']}," \
        f"{row['SETPOINT04_F03']}," \
        f"{row['BFIC_3002_F03_MV']}"

        producer.send(conf.KAFKA_OPT_SRC_TOPIC, msg)
        time.sleep(5)


if __name__ == '__main__':
    df = pd.read_csv("/root/works/idata/ma16_data/origin_data/优化分析1/predic_data/多氟多_在线数据.csv")
    # print(df)

    while True:
        send_data_2_kafka(df)

