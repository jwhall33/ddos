import warnings
import json

from elasticsearch import Elasticsearch
import re

try:

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        es = Elasticsearch(
            hosts="localhost",
            port=9200,
            timeout=600
        )
        regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "-" "(.*?)"'

        logFile = open("apache-access-log.txt")
        i = 1
        for line in logFile.readlines():
            data = re.match(regex, line).groups()
            str = '{"ip-address":"'+data[0]+'", "timestamp":"'+data[1]+'", "request":"'+data[2]+'", "status":"'+data[3]+'", "bytes":"'+data[4]+'", "agent":"'+data[5]+'"}'
            es.index(index="httplog", body=str)


except Exception as e:
    print(e)