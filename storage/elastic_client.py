from datetime import datetime
from logging import Logger
from elasticsearch import Elasticsearch


class ElasticsearchClient:
    def __init__(self, es_uri: str, index_name: str, logger: Logger, mapping: dict):
        self.es_uri = es_uri
        self.index_name = index_name
        self.logger = logger
        self.mapping = mapping
        self.client = None

    def connect(self):
        if self.client is None:
            try:
                self.logger.info("Connecting to elastic search")
                self.client = Elasticsearch(self.es_uri)
                if not self.client.ping():
                    raise ConnectionError(f"the server {self.es_uri} is unavailable!")
            except Exception as e:
                self.logger.error(f"Failed connecting to elastic: {str(e)}")
                raise
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(index=self.index_name, body=self.mapping)

    def upsert(self, document, audio_id: int):
        self.connect()

        timestamp = datetime.now().isoformat()
        document['updated_at'] = timestamp
        body = {
            'doc': document,
            'upsert': {**document, 'created_at': timestamp}
        }

        try:
            response = self.client.update(index=self.index_name, id=audio_id, body=body, refresh=True)
            self.logger.info(f"document (id: {audio_id}) {response['result']}.")
        except Exception as e:
            self.logger.error(f"Failed to upsert document {audio_id}: {str(e)}")
