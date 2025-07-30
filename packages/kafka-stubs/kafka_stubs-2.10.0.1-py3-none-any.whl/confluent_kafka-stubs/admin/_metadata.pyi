from confluent_kafka.cimpl import KafkaError

class ClusterMetadata:
    cluster_id: str | None
    controller_id: int
    brokers: dict[int, BrokerMetadata]
    topics: dict[str, TopicMetadata]
    orig_broker_id: int
    orig_broker_name: str | None

    def __init__(self) -> None: ...

class BrokerMetadata:
    id: int
    host: str | None
    port: int

    def __init__(self) -> None: ...

class TopicMetadata:
    topic: str | None
    partitions: dict[int, PartitionMetadata]
    error: KafkaError | None

    def __init__(self) -> None: ...

class PartitionMetadata:
    id: int
    leader: int
    replicas: list[int]
    isr: list[int]
    error: KafkaError | None

    def __init__(self) -> None: ...

class GroupMember:
    id: str | None
    client_id: str | None
    client_host: str | None
    metadata: bytes | None
    assignment: bytes | None

    def __init__(self) -> None: ...
