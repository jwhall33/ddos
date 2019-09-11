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
