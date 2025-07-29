from orjson import dumps, loads
from sopsy import Sops, SopsyInOutType
from os import path
from pathlib import Path
from shutil import move
from datetime import datetime


class Cache:
    """Mechanism for sealing and protecting a dataset at rest for commiting to git"""

    def __init__(self, sops_file: str, file_type: SopsyInOutType):
        self.sops_file = Path(sops_file)
        self.file_type = file_type
        self.data = {}

        sops_kwargs = {
            "file": self.sops_file,
            "input_type": self.file_type,
            "output_type": self.file_type,
        }

        # Dumnmy file creation, or else sops will throw exception
        if path.exists(sops_file):
            created = False
        else:
            created = True
            with open(sops_file, "a"):
                pass

        # We want to ingest the data, not overwrite the file yet
        self.sops_reader: Sops = Sops(in_place=False, **sops_kwargs)
        self.sops_writer: Sops = Sops(in_place=True, **sops_kwargs)

        # only unseal if the file existed
        if not created:
            self._load()

    def _load(self):
        """Unseal the dataset"""
        try:
            raw_string = self.sops_reader.decrypt(to_dict=False)
        except:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"archive-{timestamp}-{self.sops_file.name}"
            new_path = Path(self.sops_file.parent / new_file_name)
            move(self.sops_file, new_path)
            print(
                f"[CacheGuard] Warning: Cache JSON error - old cache potentially corrupt or empty.\n - Created new one and archived original at: {new_path}"
            )
            return  # The file was not valid and was empty or corrupt
        else:
            assert type(raw_string) == bytes
            decoded_string = raw_string.decode()
            self.data = loads(decoded_string)

    def _save(self):
        """Write the dataset to the encrypted at-rest state"""

        with open(self.sops_file, "w") as file:
            file.write(dumps(self.data).decode())

        self.sops_writer.encrypt()

    def add(self, entry: dict):
        """Add a new entry"""
        self.data = {**self.data, **entry}


# Local pre-release testing
if __name__ == "__main__":
    cache = Cache("secrets/cache.bin", SopsyInOutType.BINARY)
    cache.add({"something": "thing"})
    cache._save()
    print(cache)
