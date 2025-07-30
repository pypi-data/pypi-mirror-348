from confluent_kafka.cimpl import KafkaError as KafkaError, KafkaException as KafkaException, Message
from confluent_kafka.serialization import SerializationError

class _KafkaClientError(KafkaException):
    exception: Exception | None
    kafka_message: Message | None

    def __init__(
        self, kafka_error: KafkaError, exception: Exception | None = None, kafka_message: Message | None = None
    ) -> None: ...
    @property
    def code(self) -> int: ...
    @property
    def name(self) -> str: ...

class ConsumeError(_KafkaClientError): ...

class KeyDeserializationError(ConsumeError, SerializationError):
    def __init__(self, exception: Exception | None = None, kafka_message: Message | None = None) -> None: ...

class ValueDeserializationError(ConsumeError, SerializationError):
    def __init__(self, exception: Exception | None = None, kafka_message: Message | None = None) -> None: ...

class ProduceError(_KafkaClientError):
    def __init__(self, kafka_error: KafkaError, exception: KafkaException | None = None) -> None: ...

class KeySerializationError(ProduceError, SerializationError):
    def __init__(self, exception: Exception | None = None) -> None: ...

class ValueSerializationError(ProduceError, SerializationError):
    def __init__(self, exception: Exception | None = None) -> None: ...
