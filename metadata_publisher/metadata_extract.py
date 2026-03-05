from pathlib import Path
from datetime import datetime, timezone


class MetadataExtract:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def extract_size(self):
        return self.file_path.stat().st_size

    def extract_ctime(self):
        ctime = datetime.fromtimestamp(self.file_path.stat().st_ctime, tz=timezone.utc)
        return ctime.strftime("%d-%m-%Y %H:%M:%S.%f")

    def extract_name(self):
        return self.file_path.name

    def extract_all_metadata(self):
        return {'name': self.extract_name(), 'size': self.extract_size(), 'ctime': self.extract_ctime()}

    def extract_all_to_json(self):
        return {'path': str(self.file_path), 'metadata': self.extract_all_metadata()}


