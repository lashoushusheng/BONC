# !/usr/bin/python
# -*- coding: utf-8 -*-

from CConfig import conf
import paho.mqtt.client as mqtt
import pandas as pd
import json
import time

import paho.mqtt.publish as publish

from DPublic.MyLog import MyLog

logFname = '{}/rtc_kafka_2db.log'.format(conf.LOG_PATH)
mylog = MyLog(logFname, level=conf.LOG_LEVEL).logger


class soft_Result_mqtt(object):
    """
    kafka to mqtt
    """
    def __init__(self):
        pass

    def process_all_time(self):
        while True:
            self.process_one_time()
            time.sleep(10)

    def process_one_time(self):
        """
        """
        client = mqtt.Client(     # 4, 就是MQTT3.1.1
            client_id=conf.EMQ_PRODUCER_ID, userdata=None, protocol=4
        )

        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect

        client.username_pw_set(   # 设置用户密码，如果没有设置用户，可以省略
            conf.EMQ_USER, conf.EMQ_PASSWORD
        )
        client.connect(
            host=conf.EMQ_HOST, port=conf.EMQ_PORT, keepalive=conf.EMQ_PRODUCER_KEEPALIVE
        )
        client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        """
        """
        # 连接, 成功.
        if rc == 0:
            mylog.info("emq connect ok...rc=[{}]".format(str(rc)))
            self.publish_topic(client)
            client.disconnect()

        # 连接, 失败.
        else:
            mylog.error("emq connect fail !")
            client.disconnect()

    def on_disconnect(self, client, userdata, rc):
        """
            rc：操作结果状态码. 0 代表成功.
        """
        mylog.info("emq disconnect...rc=[{}]".format(str(rc)))

    def publish_topic(self, client):
        """
            向Emq，发送数据.
        """
        try:
            for index, row in self.read_soft_result().iterrows():
                msg = {"time": row['time'], "prediction": row['prediction']}
                res = client.publish(
                    topic=conf.EMQ_TOPIC, payload=json.dumps(msg), qos=0)

                if res.is_published:
                    mylog.info("emq_producer pub message ok, With mid=[{}]...msg=[{}]".format(res.mid, json.dumps(msg)))
                else:
                    mylog.error("emq_producer pub message fail !")

        except ValueError as err_str:
            mylog.error("emq_producer pub error...[{}] ".format(err_str))

    def read_soft_result(self):
        df = pd.read_csv("/root/works/idata/ma16_data/产品质量软测量/质量软测量_2#B/predict_result/aa.csv")
        # print(df)
        # for index, row in df.iterrows():
        #     print(index, row['time'], row['prediction'])
        return df


if __name__ == '__main__':
    result = soft_Result_mqtt()
    # result.process_one_time()
    result.process_all_time()
    # result.read_soft_result()
