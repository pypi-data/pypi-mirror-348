from pathlib import Path
from typing import Never, TypeAlias

try:
    from avro.schema import Schema
except ModuleNotFoundError:
    Schema: TypeAlias = Never  # type: ignore[no-redef]

def loads(schema_str: str) -> Schema: ...
def load(fp: str | Path) -> Schema: ...
