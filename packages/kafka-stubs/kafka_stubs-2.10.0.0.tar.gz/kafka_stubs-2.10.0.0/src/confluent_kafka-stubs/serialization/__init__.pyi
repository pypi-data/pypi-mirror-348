from enum import Enum
from typing import Generic, TypeVar

from confluent_kafka.error import KafkaException

_T_co = TypeVar('_T_co', covariant=True)
_T_contra = TypeVar('_T_contra', contravariant=True)

__all__ = [
    'Deserializer',
    'DoubleDeserializer',
    'DoubleSerializer',
    'IntegerDeserializer',
    'IntegerSerializer',
    'MessageField',
    'SerializationContext',
    'SerializationError',
    'Serializer',
    'StringDeserializer',
    'StringSerializer',
]

class MessageField(str, Enum):
    NONE = ...
    KEY = ...
    VALUE = ...

class SerializationContext:
    topic: str
    field: MessageField
    headers: list[tuple[str, str | bytes | None]] | None

    def __init__(
        self, topic: str, field: MessageField, headers: list[tuple[str, str | bytes | None]] | None = None
    ) -> None: ...

class SerializationError(KafkaException): ...

class Serializer(Generic[_T_contra]):
    def __call__(self, obj: _T_contra | None, ctx: SerializationContext | None = None) -> bytes | None: ...

class Deserializer(Generic[_T_co]):
    def __call__(self, value: bytes | None, ctx: SerializationContext | None = None) -> _T_co | None: ...

class DoubleSerializer(Serializer[float]): ...
class DoubleDeserializer(Deserializer[float]): ...
class IntegerSerializer(Serializer[int]): ...
class IntegerDeserializer(Deserializer[int]): ...

class StringSerializer(Serializer[str]):
    def __init__(self, codec: str = 'utf_8') -> None: ...

class StringDeserializer(Deserializer):
    def __init__(self, codec: str = 'utf_8') -> None: ...
