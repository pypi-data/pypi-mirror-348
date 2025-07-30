import logging
from concurrent.futures import Future
from typing import Any, Literal, overload

from confluent_kafka._model import (
    ConsumerGroupState,
    ConsumerGroupTopicPartitions,
    ConsumerGroupType,
    ElectionType,
    IsolationLevel,
    TopicCollection,
)
from confluent_kafka.admin._acl import (
    AclBinding as AclBinding,
    AclBindingFilter as AclBindingFilter,
    AclOperation as AclOperation,
    AclPermissionType as AclPermissionType,
)
from confluent_kafka.admin._cluster import DescribeClusterResult as DescribeClusterResult
from confluent_kafka.admin._config import (
    AlterConfigOpType as AlterConfigOpType,
    ConfigEntry as ConfigEntry,
    ConfigResource as ConfigResource,
    ConfigSource as ConfigSource,
)
from confluent_kafka.admin._group import (
    ConsumerGroupDescription as ConsumerGroupDescription,
    ConsumerGroupListing as ConsumerGroupListing,
    ListConsumerGroupsResult as ListConsumerGroupsResult,
    MemberAssignment as MemberAssignment,
    MemberDescription as MemberDescription,
)
from confluent_kafka.admin._listoffsets import ListOffsetsResultInfo as ListOffsetsResultInfo, OffsetSpec as OffsetSpec
from confluent_kafka.admin._metadata import (
    BrokerMetadata as BrokerMetadata,
    ClusterMetadata as ClusterMetadata,
    GroupMember as GroupMember,
    PartitionMetadata as PartitionMetadata,
    TopicMetadata as TopicMetadata,
)
from confluent_kafka.admin._records import DeletedRecords as DeletedRecords
from confluent_kafka.admin._resource import ResourcePatternType as ResourcePatternType, ResourceType as ResourceType
from confluent_kafka.admin._scram import (
    ScramCredentialInfo as ScramCredentialInfo,
    ScramMechanism as ScramMechanism,
    UserScramCredentialAlteration as UserScramCredentialAlteration,
    UserScramCredentialDeletion as UserScramCredentialDeletion,
    UserScramCredentialsDescription as UserScramCredentialsDescription,
    UserScramCredentialUpsertion as UserScramCredentialUpsertion,
)
from confluent_kafka.admin._topic import TopicDescription as TopicDescription
from confluent_kafka.cimpl import (
    CONFIG_SOURCE_DEFAULT_CONFIG as CONFIG_SOURCE_DEFAULT_CONFIG,
    CONFIG_SOURCE_DYNAMIC_BROKER_CONFIG as CONFIG_SOURCE_DYNAMIC_BROKER_CONFIG,
    CONFIG_SOURCE_DYNAMIC_DEFAULT_BROKER_CONFIG as CONFIG_SOURCE_DYNAMIC_DEFAULT_BROKER_CONFIG,
    CONFIG_SOURCE_DYNAMIC_TOPIC_CONFIG as CONFIG_SOURCE_DYNAMIC_TOPIC_CONFIG,
    CONFIG_SOURCE_GROUP_CONFIG as CONFIG_SOURCE_GROUP_CONFIG,
    CONFIG_SOURCE_STATIC_BROKER_CONFIG as CONFIG_SOURCE_STATIC_BROKER_CONFIG,
    CONFIG_SOURCE_UNKNOWN_CONFIG as CONFIG_SOURCE_UNKNOWN_CONFIG,
    OFFSET_INVALID as OFFSET_INVALID,
    RESOURCE_ANY as RESOURCE_ANY,
    RESOURCE_BROKER as RESOURCE_BROKER,
    RESOURCE_GROUP as RESOURCE_GROUP,
    RESOURCE_TOPIC as RESOURCE_TOPIC,
    RESOURCE_TRANSACTIONAL_ID as RESOURCE_TRANSACTIONAL_ID,
    RESOURCE_UNKNOWN as RESOURCE_UNKNOWN,
    KafkaError as KafkaError,
    KafkaException as KafkaException,
    NewPartitions as NewPartitions,
    NewTopic as NewTopic,
    TopicPartition,
)

class AdminClient:
    def __init__(self, conf: dict[str, Any], logger: logging.Logger | None = None) -> None: ...
    def create_topics(
        self,
        new_topics: list[NewTopic],
        *,
        operation_timeout: float = ...,
        request_timeout: float = ...,
        validate_only: bool = False,
    ) -> dict[str, Future[None]]: ...
    def delete_topics(
        self, topics: list[str], *, operation_timeout: float = ..., request_timeout: float = ...
    ) -> dict[str, Future[None]]: ...
    def list_topics(self, topic: str | None = None, timeout: float = ...) -> ClusterMetadata: ...
    def list_groups(self, group: str | None = None, timeout: float = ...) -> Future[ListConsumerGroupsResult]: ...
    def create_partitions(
        self,
        new_partitions: list[NewPartitions],
        *,
        operation_timeout: float = ...,
        request_timeout: float = ...,
        validate_only: bool = False,
    ) -> dict[str, Future[None]]: ...
    def describe_configs(
        self, resources: list[ConfigResource], *, request_timeout: float = ...
    ) -> dict[ConfigResource, Future[dict[str, ConfigEntry]]]: ...
    def alter_configs(
        self, resources: list[ConfigResource], *, request_timeout: float = ..., validate_only: bool = False
    ) -> dict[ConfigResource, Future[None]]: ...
    def incremental_alter_configs(
        self,
        resources: list[ConfigResource],
        *,
        request_timeout: float = ...,
        validate_only: bool = False,
        broker: int = ...,
    ) -> dict[ConfigResource, Future[None]]: ...
    def create_acls(
        self, acls: list[AclBinding], *, request_timeout: float = ...
    ) -> dict[AclBinding, Future[None]]: ...
    def describe_acls(
        self, acl_binding_filter: AclBindingFilter, *, request_timeout: float = ...
    ) -> Future[list[AclBinding]]: ...
    def delete_acls(
        self, acl_binding_filters: list[AclBindingFilter], *, request_timeout: float = ...
    ) -> dict[AclBindingFilter, Future[list[AclBinding]]]: ...
    def list_consumer_groups(
        self,
        *,
        request_timeout: float = ...,
        states: set[ConsumerGroupState] = ...,
        types: set[ConsumerGroupType] = ...,
    ) -> Future[ListConsumerGroupsResult]: ...
    def describe_consumer_groups(
        self, group_ids: list[str], *, include_authorized_operations: bool = False, request_timeout: float = ...
    ) -> dict[str, Future[ConsumerGroupDescription]]: ...
    def describe_topics(
        self, topics: TopicCollection, *, include_authorized_operations: bool = False, request_timeout: float = ...
    ) -> dict[str, Future[TopicDescription]]: ...
    def describe_cluster(
        self, *, include_authorized_operations: bool = False, request_timeout: float = ...
    ) -> Future[DescribeClusterResult]: ...
    def delete_consumer_groups(
        self, group_ids: list[str], *, request_timeout: float = ...
    ) -> dict[str, Future[None]]: ...
    def list_consumer_group_offsets(
        self,
        list_consumer_group_offsets_request: list[ConsumerGroupTopicPartitions],
        *,
        require_stable: bool = False,
        request_timeout: float = ...,
    ) -> dict[str, Future[ConsumerGroupTopicPartitions]]: ...
    def alter_consumer_group_offsets(
        self,
        alter_consumer_group_offsets_request: list[ConsumerGroupTopicPartitions],
        *,
        request_timeout: float = ...,
    ) -> dict[ConsumerGroupTopicPartitions, Future[ConsumerGroupTopicPartitions]]: ...
    def set_sasl_credentials(self, username: str, password: str) -> None: ...
    @overload
    def describe_user_scram_credentials(
        self, users: Literal[None] = None, *, request_timeout: float = ...
    ) -> Future[dict[str, UserScramCredentialsDescription]]: ...
    @overload
    def describe_user_scram_credentials(
        self, users: list[str], *, request_timeout: float = ...
    ) -> dict[str, Future[UserScramCredentialsDescription]]: ...
    @overload
    def describe_user_scram_credentials(
        self, users: list[str] | None = None, *, request_timeout: float = ...
    ) -> Future[dict[str, UserScramCredentialsDescription]] | dict[str, Future[UserScramCredentialsDescription]]: ...
    def alter_user_scram_credentials(
        self, alterations: list[UserScramCredentialAlteration], *, request_timeout: float = ...
    ) -> dict[str, Future[None]]: ...
    def list_offsets(
        self,
        topic_partition_offsets: dict[TopicPartition, OffsetSpec],
        *,
        isolation_level: IsolationLevel = ...,
        request_timeout: float = ...,
    ) -> dict[str, Future[ListOffsetsResultInfo]]: ...
    def delete_records(
        self,
        topic_partition_offsets: list[TopicPartition],
        *,
        request_timeout: float = ...,
        operation_timeout: float = ...,
    ) -> dict[TopicPartition, Future[DeletedRecords]]: ...
    def elect_leaders(
        self,
        election_type: ElectionType,
        partitions: list[TopicPartition] | None = None,
        *,
        request_timeout: float = ...,
        operation_timeout: float = ...,
    ) -> Future[dict[TopicPartition, KafkaException | None]]: ...
    def poll(self, timeout: float) -> int: ...
