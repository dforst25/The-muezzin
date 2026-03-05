from confluent_kafka import Producer
from logging import Logger


class KafkaPublisher:
    def __init__(self, logger: Logger, bootstrap_servers, topic_name):
        self.logger = logger
        self.bootstrap_servers = bootstrap_servers
        self.topic_name = topic_name
        self.producer = None

    def publish(self, event):
        def delivery_report(err, msg):
            if err:
                self.logger.error(f"Delivery failed: {err}")
            else:
                self.logger.info(f"Delivered {msg.value().decode('utf-8')}")
                self.logger.info(f"Delivered to {msg.topic()} : partition {msg.partition()} : at offset {msg.offset()}")
        if self.producer is None:
            self.producer = Producer({"bootstrap.servers": self.bootstrap_servers})
        self.logger.info("connecting to Kafka topic...")
        self.producer.poll(1.0)
        self.producer.produce(topic=self.topic_name, value=event, callback=delivery_report)
        self.producer.flush()
