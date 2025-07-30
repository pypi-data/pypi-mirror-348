# Python Modules
from datetime import datetime
from enum import Enum
from os import path
from pathlib import Path
from shutil import move

# Third-Party Modules
from sopsy import Sops, SopsyInOutType, SopsyUnparsableOutpoutTypeError


class CacheType(Enum):
    JSON = "json"
    TEXT = "text"


class BaseCache:
    """Mechanism for sealing and protecting a dataset at rest for commiting to git"""

    def __init__(self, sops_file: str):
        self.sops_file = Path(sops_file)

        sops_kwargs = {
            "file": self.sops_file,
            "input_type": SopsyInOutType.BINARY,
            "output_type": SopsyInOutType.BINARY,
        }

        # Dumnmy file creation, or else sops will throw exception
        if path.exists(sops_file):
            created = False
        else:
            created = True
            Path(sops_file).parent.mkdir(parents=True, exist_ok=True)
            Path(sops_file).touch(exist_ok=True)

        # We want to ingest the data, not overwrite the file yet
        self.sops_reader: Sops = Sops(in_place=False, **sops_kwargs)
        self.sops_writer: Sops = Sops(in_place=True, **sops_kwargs)

        # only unseal if the file existed
        if not created:
            self.load()

    def load(self) -> str:
        """Unseal the dataset"""
        try:
            raw_string = self.sops_reader.decrypt(to_dict=False)
        except (OSError, SopsyUnparsableOutpoutTypeError):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"archive-{timestamp}-{self.sops_file.name}"
            new_path = Path(self.sops_file.parent / new_file_name)
            move(self.sops_file, new_path)
            print(
                f"[CacheGuard] Warning: Cache JSON error - old cache potentially corrupt or empty.\n - Created new one and archived original at: {new_path}"
            )
            return ""  # The file was not valid and was empty or corrupt
        else:
            # we request only a bytes object, so that's all we get
            output_string = raw_string.decode()  # type: ignore
            return output_string

    def save(self) -> None:
        """Write the dataset to the encrypted at-rest state"""
        self.sops_writer.encrypt()
