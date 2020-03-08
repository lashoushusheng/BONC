from kafka import KafkaProducer
import json

'''
 5     生产者demo
 6     向test_lyl2主题中循环写入10条json数据
 7     注意事项：要写入json数据需加上value_serializer参数，如下代码
 8 '''
producer = KafkaProducer(
    value_serializer=lambda v: v.encode('utf-8'),
    bootstrap_servers=['192.168.100.2:9092']
)
for i in range(10):
     data= "hello world!"
     producer.send('ma16_src_soft_measure', data)

producer.close()