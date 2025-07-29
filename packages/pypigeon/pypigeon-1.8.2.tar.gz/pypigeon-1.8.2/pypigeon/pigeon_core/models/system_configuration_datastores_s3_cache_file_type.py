from enum import Enum


class SystemConfigurationDatastoresS3CacheFileType(str, Enum):
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
