from enum import Enum


class SystemConfigurationDatastoresS3CacheMemType(str, Enum):
    MEM = "mem"

    def __str__(self) -> str:
        return str(self.value)
