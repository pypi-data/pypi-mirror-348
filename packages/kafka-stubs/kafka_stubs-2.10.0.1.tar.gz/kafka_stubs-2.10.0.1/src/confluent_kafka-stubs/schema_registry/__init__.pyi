from confluent_kafka.schema_registry.error import SchemaRegistryError
from confluent_kafka.schema_registry.schema_registry_client import (
    ConfigCompatibilityLevel,
    Metadata,
    MetadataProperties,
    MetadataTags,
    RegisteredSchema,
    Rule,
    RuleKind,
    RuleMode,
    RuleParams,
    RuleSet,
    Schema,
    SchemaReference,
    SchemaRegistryClient,
    ServerConfig,
)
from confluent_kafka.serialization import SerializationContext

_MAGIC_BYTE = ...
__all__ = [
    'ConfigCompatibilityLevel',
    'Metadata',
    'MetadataProperties',
    'MetadataTags',
    'RegisteredSchema',
    'Rule',
    'RuleKind',
    'RuleMode',
    'RuleParams',
    'RuleSet',
    'Schema',
    'SchemaReference',
    'SchemaRegistryClient',
    'SchemaRegistryError',
    'ServerConfig',
    'record_subject_name_strategy',
    'topic_record_subject_name_strategy',
    'topic_subject_name_strategy',
]

def topic_subject_name_strategy(ctx: SerializationContext, record_name: str | None) -> str | None: ...
def topic_record_subject_name_strategy(ctx: SerializationContext, record_name: str | None) -> str | None: ...
def record_subject_name_strategy(ctx: SerializationContext, record_name: str | None) -> str | None: ...
def reference_subject_name_strategy(ctx: SerializationContext, schema_ref: SchemaReference) -> str | None: ...
