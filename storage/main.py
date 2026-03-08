import os

from kafka_consumer import KafkaConsumer
from grid_FS_storage import GridFSStorage
from elastic_client import ElasticsearchClient
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("storage-service")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "METADATA")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "storage-service")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

ELASTIC_URI = os.getenv("ELASTIC_URI", 'http://localhost:9200')
INDEX_NAME = os.getenv("INDEX_NAME", 'processed_audio')


def main():
    consumer = KafkaConsumer(KAFKA_BOOTSTRAP_SERVERS, TOPIC_NAME, KAFKA_GROUP_ID, logger)

    storage = GridFSStorage(MONGO_URI, logger)

    mapping = {
        'mappings': {
            'properties': {
                'audio_id': {'type': 'long'},
                'path': {'type': 'text'},
                "metadata": {
                    "properties": {
                        "name": {"type": "keyword"},
                        "size": {"type": "long"},
                        "ctime": {"type": "date", "format": "dd-MM-yyyy HH:mm:ss.SSSSSS"},
                    }
                },
                'created_at': {'type': 'date'},
                'updated_at': {'type': 'date'}
            }
        }
    }
    elastic_client = ElasticsearchClient(ELASTIC_URI, INDEX_NAME, logger, mapping)
    while True:
        audio = consumer.start_callback()
        name = audio['metadata']['name']
        logger.info(f"generating for audio {name} an id...")
        audio_id = hash(name)
        logger.info(f"the id is: {audio_id}.")
        audio['audio_id'] = audio_id
        elastic_client.upsert(document=audio, audio_id=audio_id)
        with open(audio['path'], 'rb') as f:
            logger.info("Sending the binary file to mongo...")
            storage.save(f.read(), audio_id, name)


if __name__ == "__main__":
    main()
