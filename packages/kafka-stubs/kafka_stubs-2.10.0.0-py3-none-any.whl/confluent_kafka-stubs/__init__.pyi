from confluent_kafka._model import (
    ConsumerGroupState,
    ConsumerGroupTopicPartitions,
    ConsumerGroupType,
    ElectionType as ElectionType,
    IsolationLevel,
    Node,
    TopicCollection,
    TopicPartitionInfo,
)
from confluent_kafka.cimpl import (
    OFFSET_BEGINNING,
    OFFSET_END,
    OFFSET_INVALID,
    OFFSET_STORED,
    TIMESTAMP_CREATE_TIME,
    TIMESTAMP_LOG_APPEND_TIME,
    TIMESTAMP_NOT_AVAILABLE,
    Consumer,
    Message,
    Producer,
    TopicPartition,
    Uuid,
    libversion,
)
from confluent_kafka.deserializing_consumer import DeserializingConsumer
from confluent_kafka.error import KafkaError, KafkaException
from confluent_kafka.serializing_producer import SerializingProducer

__all__ = [
    'OFFSET_BEGINNING',
    'OFFSET_END',
    'OFFSET_INVALID',
    'OFFSET_STORED',
    'TIMESTAMP_CREATE_TIME',
    'TIMESTAMP_LOG_APPEND_TIME',
    'TIMESTAMP_NOT_AVAILABLE',
    'Consumer',
    'ConsumerGroupState',
    'ConsumerGroupTopicPartitions',
    'ConsumerGroupType',
    'DeserializingConsumer',
    'IsolationLevel',
    'KafkaError',
    'KafkaException',
    'Message',
    'Node',
    'Producer',
    'SerializingProducer',
    'TopicCollection',
    'TopicPartition',
    'TopicPartitionInfo',
    'Uuid',
    'libversion',
]
__version__ = ...

class ThrottleEvent:
    broker_name: str
    broker_id: int
    throttle_time: float
    def __init__(self, broker_name: str, broker_id: int, throttle_time: float) -> None: ...
