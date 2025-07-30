from sopsy import SopsyInOutType
from cacheguard.base_cache import BaseCache

from orjson import dumps, loads


class KeyCache(BaseCache):
    """Key-Value edition of the Cache"""

    def __init__(self, sops_file: str, file_type: SopsyInOutType):
        self.data = {}
        super().__init__(sops_file, file_type)

    def load(self) -> str:
        """Handle the data for key-values by loading with JSON"""
        self.data = loads(super().load())
        return self.data

    def save(self):
        """Write the dataset to the encrypted at-rest state"""
        with open(self.sops_file, "w") as file:
            file.write(dumps(self.data).decode())
        super().save()

    def add(self, entry: dict):
        """Add a new entry"""
        self.data = {**self.data, **entry}
