from logging import Logger
from gridfs import GridFS
from pymongo import MongoClient


class GridFSStorage:
    def __init__(self, mongo_uri: str, logger: Logger):
        self.mongo_uri = mongo_uri
        self.logger = logger

    def save(self, file_stream, audio_id, file_name):
        try:
            client = MongoClient(self.mongo_uri)
            db = client["files_db"]
            fs = GridFS(db)
            self.logger.info("Successfully connected to MongoDB GridFS")
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

        try:
            self.logger.info(f"Saving binary data for audio_id: {audio_id}")
            file_id = fs.put(file_stream, _id=audio_id, filename=file_name)
            self.logger.info(f"File successfully saved with ID: {file_id}")
        except Exception as e:
            self.logger.error(f"Error saving to GridFS: {e}")
        finally:
            client.close()
