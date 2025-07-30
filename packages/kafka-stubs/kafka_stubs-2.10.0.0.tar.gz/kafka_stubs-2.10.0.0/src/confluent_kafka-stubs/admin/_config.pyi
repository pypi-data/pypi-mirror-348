from enum import Enum
from typing import Any

from confluent_kafka import KafkaError
from confluent_kafka.admin._resource import ResourceType

class AlterConfigOpType(Enum):
    SET = ...
    DELETE = ...
    APPEND = ...
    SUBTRACT = ...

class ConfigSource(Enum):
    UNKNOWN_CONFIG = ...
    DYNAMIC_TOPIC_CONFIG = ...
    DYNAMIC_BROKER_CONFIG = ...
    DYNAMIC_DEFAULT_BROKER_CONFIG = ...
    STATIC_BROKER_CONFIG = ...
    DEFAULT_CONFIG = ...
    GROUP_CONFIG = ...

class ConfigEntry:
    name: str
    value: str | None
    source: ConfigSource
    is_read_only: bool
    is_default: bool
    is_sensitive: bool
    is_synonym: bool
    synonyms: list[ConfigEntry]
    incremental_operation: AlterConfigOpType | None

    def __init__(
        self,
        name: str,
        value: str | None,
        source: ConfigSource = ...,
        is_read_only: bool = False,
        is_default: bool = False,
        is_sensitive: bool = False,
        is_synonym: bool = False,
        synonyms: list[ConfigEntry] = ...,
        incremental_operation: AlterConfigOpType | None = None,
    ) -> None: ...

class ConfigResource:
    Type: type[ResourceType] = ...

    restype: ResourceType
    restype_int: int
    name: str
    set_config_dict: dict[str, str]
    configs: dict[str, Any] | None
    incremental_configs: list[ConfigEntry]
    error: KafkaError | None

    def __init__(
        self,
        restype: ResourceType | str | int,
        name: str,
        set_config: dict[str, str] | None = None,
        described_configs: dict[str, Any] | None = None,
        error: KafkaError | None = None,
        incremental_configs: list[ConfigEntry] | None = None,
    ) -> None: ...
    def __len__(self) -> int: ...
    def set_config(self, name: str, value: str, overwrite: bool = True) -> None: ...
    def add_incremental_config(self, config_entry: ConfigEntry) -> None: ...
