from sopsy import SopsyInOutType
from cacheguard.base_cache import BaseCache


class TextCache(BaseCache):
    """Plain-text edition of the cache"""

    def __init__(self, sops_file: str, file_type: SopsyInOutType):
        self.data = ""
        super().__init__(sops_file, file_type)

    def load(self) -> str:
        """Handle the plain text version of the cache"""
        self.data = super().load()
        return self.data

    def save(self) -> None:
        """Write the dataset to the encrypted at-rest state"""
        with open(self.sops_file, "w") as file:
            file.write(self.data)
        super().save()

    def append(self, string: str) -> None:
        """Simple method to add more string content"""
        self.data = self.data + string
