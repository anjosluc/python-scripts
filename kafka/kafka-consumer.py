from kafka import KafkaConsumer,KafkaProducer,KafkaAdminClient
from kafka.admin import NewTopic
import os
import json

def produce_kafka():
    
    #CREATE TOPIC
    #admin = KafkaAdminClient(security_protocol="SSL", bootstrap_servers=[])
    
    #new_topic = [NewTopic(name="my_topic", num_partitions=1, replication_factor=1)]
    #admin.create_topics(new_topic)
    
    #PRODUCE MESSAGES
    producer = KafkaProducer(security_protocol="SSL", bootstrap_servers=[])
    # Asynchronous by default
    for _ in range(100):
        future = producer.send('my_topic', b'raw_bytes')


def consume_kafka():
    consumer = KafkaConsumer('trade',
                         group_id='my-group', security_protocol="SSL", auto_offset_reset='earliest', enable_auto_commit=True,
                         bootstrap_servers=[])
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                            message.offset, message.key,
                                            message.value))

if __name__ == "__main__":
    consume_kafka()