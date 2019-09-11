import logging
import json
from timeit import default_timer as timer
from kafka import KafkaProducer


def main():
    startTime = timer()
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    for line in open("apache-access-log.txt"):
        producer.send('http-log', line)

    endTime = timer() - startTime
    print("Runtime: " + str(endTime))


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:' +
               '%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()


