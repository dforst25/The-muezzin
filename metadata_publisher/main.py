import os
import logging
import json
from glob import glob
from kafka_publisher import KafkaPublisher
from metadata_extract import MetadataExtract

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("metadata-publisher-service")
PODCASTS_DIR = os.getenv("PODCASTS_DIR", "../podcasts")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "METADATA")


def main():
    files = glob(f'{PODCASTS_DIR}/*.wav')
    publisher = KafkaPublisher(logger, KAFKA_BOOTSTRAP_SERVERS, TOPIC_NAME)
    for file in files:
        extract = MetadataExtract(file)
        publisher.publish(json.dumps(extract.extract_all_to_json()).encode())
    if not files:
        logger.info("There are no files!")


if __name__ == "__main__":
    main()
