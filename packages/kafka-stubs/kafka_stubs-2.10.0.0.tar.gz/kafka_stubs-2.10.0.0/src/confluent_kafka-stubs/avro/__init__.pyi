from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient as CachedSchemaRegistryClient
from confluent_kafka.avro.error import ClientError as ClientError
from confluent_kafka.avro.load import load as load, loads as loads
from confluent_kafka.avro.serializer import (
    KeySerializerError as KeySerializerError,
    SerializerError as SerializerError,
    ValueSerializerError as ValueSerializerError,
)
from confluent_kafka.avro.serializer.message_serializer import MessageSerializer as MessageSerializer
