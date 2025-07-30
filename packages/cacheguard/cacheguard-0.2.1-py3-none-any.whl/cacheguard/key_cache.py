# Project Modules
from cacheguard.base_cache import BaseCache

# Third-Party Modules
from orjson import dumps, loads


class KeyCache(BaseCache):
    """Key-Value edition of the Cache"""

    def __init__(self, sops_file: str):
        self.data = {}
        super().__init__(sops_file)

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
