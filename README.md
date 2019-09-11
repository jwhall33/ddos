# ddos
How I decided to do this:
1. decide Python was my strongest choice here
2. install [Kafka](https://kafka.apache.org)
3. review the [quickstart](https://kafka.apache.org/quickstart) guide in order to know how this works
4. after the quickstart; figure out how todo this in python  
  4a. [this was helpful for consumer/producer](https://medium.com/@mukeshkumar_46704/consume-json-messages-from-kafka-using-kafka-pythons-deserializer-859f5d39e02c)  
  4b. [this was too](https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1)
5. I really got stuck with Kafka offsets at first.  always going from the first message was easy until I started adding more data.  I went as far as deleting the data from the kafka folder and also the /tmp folder (which isn't straight forward on a mac); feeling overwhelmed, I called it a night.
6. I downloaded [ElasticSearch](https://www.elastic.co/) and [Kibana](https://www.elastic.co/start) to get a sense for what the data really is (visualization)
7. getting the data to index just right was time consuming.  ended up with a regular expression to parse the data.  This is my [friend](https://regexr.com)!
8. from there I made the decision to implement a solution already out there.  that is when I found this [https://github.com/lokeshsam55/Project_Developer](https://github.com/lokeshsam55/Project_Developer)
9. downloaded [Spark](https://spark.apache.org/)
10. and the associated jar for [kafka streaming](https://search.maven.org/search?q=a:spark-streaming-kafka-0-8-assembly_2.11)
11. Needed to update the spark_stream app a bit for Python 3  
	11a. This was one of them [https://www.python.org/dev/peps/pep-3113/](https://www.python.org/dev/peps/pep-3113/)  
	11b. I also didn't setup my environment to do this in an IDE so I just copied files around in order to get the results.
12. So now when I run spark-submit; I'm able to see the list of IP addresses and the number of log entries when they reach the threshold defined in the rdd filter.
13. If time allowed, there are a few ML implementations [here](https://github.com/lbnl-cybersecurity/ddos-detection/tree/master/detection_framework) that look appealing!  

# Setup

Run Kafka and Zookeeper  
`bin/zookeeper-server-start.sh config/zookeeper.properties &`

`bin/kafka-server-start.sh config/server.properties &`

Next, create a few topics:  
`bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic http-log --partitions 1 --replication-factor 1`

`bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic http-threat --partitions 1 --replication-factor 1`

Then I open another terminal and start a console consumer for threats:  
`bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic http-threat --from-beginning`

Now I'm ready to run spark.  For simplicity, I just copy spark_stream.py into my spark folder and run:  
`bin/spark-submit --jars jars/spark-streaming-kafka-0-10-assembly_2.11-2.4.4.jar spark_stream.py`  
(Yes, I'm trying different streaming jars; and I updated my pyspark exports for python3)  

Now in my IDE, I run my producer.py...

Then you should start to see messages in the console consumer!  
["247.219.189.52", 89]  
["133.129.191.60", 89]  
["227.6.52.250", 89]  
["233.7.245.219", 89]  
["233.33.63.76", 89]  
["91.157.33.242", 89]  
["164.5.82.157", 89]  
["35.73.43.29", 89]  
["181.66.224.69", 89]  
["72.173.153.131", 89]  
["1.92.109.196", 89]  
Processed a total of 351 messages  
