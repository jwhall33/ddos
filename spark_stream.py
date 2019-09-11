
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import time
from datetime import datetime
import json
import re

from kafka import KafkaProducer


def load_msg(msg):
    message = json.loads(msg[1])
    # print("Message: " + message)
    regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "-" "(.*?)"'
    data = re.match(regex, message).groups()
    #print(data[0])
    return data[0], 1


def update_sum(new_val, sum_val):
    if not sum_val:
        sum_val = 0
    return sum(new_val) + sum_val


def sendnotice(ipthreats):
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    for ip in ipthreats:
        producer.send('http-threat', ip)
        #print(ip)
    producer.flush()



if __name__ == '__main__':
    print('Starting the process...\n')
    start = datetime.now()
    conf = SparkConf().setAppName('DetectDDOS').setMaster('local')
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 30)
    ssc.checkpoint('checkpoint')
    kafkaParams = {'bootstrap.servers': 'localhost:9092',
                    'auto.offset.reset': 'smallest'}
    kafkaStream = KafkaUtils.createDirectStream(ssc, ['http-log'], kafkaParams)
    parsed = kafkaStream.map(load_msg)
    ipcount = parsed.updateStateByKey(update_sum)
    ipmap = ipcount.map(lambda item: (str(item[0]), item[1]))
    # this should give me 380 or so IPs
    ipsuspect = ipmap.filter(lambda item: item[1] > 88)
    ipsuspect.foreachRDD(lambda rdd: rdd.foreachPartition(sendnotice))
    ipsuspect.pprint()
    ipsuspect.saveAsTextFiles('DDOS_attacker_found_output')
    ssc.start()
    time.sleep(90)
    ssc.stop()
    # print('Waiting to terminate...')
    # ssc.awaitTermination()
    # ssc.stop()
    print('Process ended.')
    print('Time taken:', datetime.now() - start)
