import io
from typing import Any, Never, TypeAlias

try:
    from avro.schema import Schema
except ModuleNotFoundError:
    Schema: TypeAlias = Never  # type: ignore[no-redef]

from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient

MAGIC_BYTE: int = ...
HAS_FAST: bool = ...

_Record: TypeAlias = Any  # FIXME: Use correct type

class ContextStringIO(io.BytesIO): ...

class MessageSerializer:
    def __init__(
        self,
        registry_client: CachedSchemaRegistryClient,
        reader_key_schema: Schema | None = None,
        reader_value_schema: Schema | None = None,
    ) -> None: ...
    def encode_record_with_schema(self, topic: str, schema: Schema, record: _Record, is_key: bool = False) -> bytes: ...
    def encode_record_with_schema_id(self, schema_id: int, record: _Record, is_key: bool = False) -> bytes: ...
    def decode_message(self, message: str | bytes | None, is_key: bool = False) -> _Record: ...
