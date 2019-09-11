from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import time
from datetime import datetime
import json
import argparse
import re


def load_msg(msg):
    message = json.loads(msg[1])
    #print("Message: " + message)
    regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "-" "(.*?)"'
    data = re.match(regex, message).groups()
    print(data[0])
    return data[0], 1


def update_sum(new_val, sum_val):
    if not sum_val:
        sum_val = 0
    return sum(new_val) + sum_val


if __name__ == '__main__':
    print('Starting the process...\n')
    start = datetime.now()
    conf = SparkConf().setAppName('DetectDDOS').setMaster('local')
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 30)
    ssc.checkpoint('checkpoint')
    kafkaParams = {'bootstrap.servers': 'localhost:9092'}
    kafkaStream = KafkaUtils.createDirectStream(ssc, ['http-log'], kafkaParams)
    parsed = kafkaStream.map(load_msg)
    ipcount = parsed.updateStateByKey(update_sum)
    ipmap = ipcount.map(lambda item: (str(item[0]), item[1]))
    ipsuspect = ipmap.filter(lambda item: item[1] >= 50)
    ipsuspect.pprint()
    ipsuspect.saveAsTextFiles('DDOS_attacker_found_output')
    ssc.start()
    time.sleep(60)
    ssc.stop()
    #print('Waiting to terminate...')
    #ssc.awaitTermination()
    #ssc.stop()
    print('Process ended.')
    print('Time taken:', datetime.now() - start)
