from confluent_kafka._model import TopicPartitionInfo
from confluent_kafka.admin._acl import AclOperation
from confluent_kafka.cimpl import Uuid

class TopicDescription:
    name: str
    topic_id: Uuid
    is_internal: bool
    partitions: list[TopicPartitionInfo]
    authorized_operations: list[AclOperation] | None

    def __init__(
        self,
        name: str,
        topic_id: Uuid,
        is_internal: bool,
        partitions: list[TopicPartitionInfo],
        authorized_operations: list[AclOperation] | None = None,
    ) -> None: ...
