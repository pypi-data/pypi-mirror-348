from collections.abc import Iterable

from confluent_kafka._model import ConsumerGroupState, ConsumerGroupType, Node
from confluent_kafka.admin._acl import AclOperation
from confluent_kafka.cimpl import KafkaException, TopicPartition

class ConsumerGroupListing:
    group_id: str
    is_simple_consumer_group: bool
    state: ConsumerGroupState
    type: ConsumerGroupType

    def __init__(
        self,
        group_id: str,
        is_simple_consumer_group: bool,
        state: ConsumerGroupState | int | None = None,
        type: ConsumerGroupType | int | None = None,
    ) -> None: ...

class ListConsumerGroupsResult:
    valid: list[ConsumerGroupListing]
    errors: list[KafkaException]

    def __init__(
        self, valid: list[ConsumerGroupListing] | None = None, errors: list[KafkaException] | None = None
    ) -> None: ...

class MemberAssignment:
    topic_partitions: list[TopicPartition]

    def __init__(self, topic_partitions: list[TopicPartition] | None = ...) -> None: ...

class MemberDescription:
    member_id: str
    client_id: str
    host: str
    assignment: MemberAssignment
    group_instance_id: str | None
    target_assignment: MemberAssignment | None

    def __init__(
        self,
        member_id: str,
        client_id: str,
        host: str,
        assignment: MemberAssignment,
        group_instance_id: str | None = None,
        target_assignment: MemberAssignment | None = None,
    ) -> None: ...

class ConsumerGroupDescription:
    group_id: str
    is_simple_consumer_group: bool
    members: list[MemberDescription]
    partition_assignor: str
    state: ConsumerGroupState
    type: ConsumerGroupType
    coordinator: Node
    authorized_operations: list[AclOperation] | None

    def __init__(
        self,
        group_id: str,
        is_simple_consumer_group: bool,
        members: list[MemberDescription],
        partition_assignor: str,
        state: ConsumerGroupState | int | str | None,
        coordinator: Node,
        authorized_operations: Iterable[AclOperation | int | str] | None = None,
        type: ConsumerGroupType | int | str | None = None,
    ) -> None: ...
