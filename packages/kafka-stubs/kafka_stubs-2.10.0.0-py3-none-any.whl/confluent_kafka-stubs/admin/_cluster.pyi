from collections.abc import Iterable

from confluent_kafka._model import Node
from confluent_kafka.admin._acl import AclOperation

class DescribeClusterResult:
    controller: Node
    nodes: list[Node]
    cluster_id: str | None
    authorized_operations: list[AclOperation] | None

    def __init__(
        self,
        controller: Node,
        nodes: list[Node],
        cluster_id: str | None = None,
        authorized_operations: Iterable[AclOperation | int | float] | None = None,
    ) -> None: ...
