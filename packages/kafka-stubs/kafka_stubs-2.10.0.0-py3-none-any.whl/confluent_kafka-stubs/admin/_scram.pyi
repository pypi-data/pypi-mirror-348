from enum import Enum

class ScramMechanism(Enum):
    UNKNOWN = ...
    SCRAM_SHA_256 = ...
    SCRAM_SHA_512 = ...

class ScramCredentialInfo:
    mechanism: ScramMechanism
    iterations: int

    def __init__(self, mechanism: ScramMechanism, iterations: int) -> None: ...

class UserScramCredentialsDescription:
    user: str
    scram_credential_infos: list[ScramCredentialInfo]

    def __init__(self, user: str, scram_credential_infos: list[ScramCredentialInfo]) -> None: ...

class UserScramCredentialAlteration:
    user: str

    def __init__(self, user: str) -> None: ...

class UserScramCredentialUpsertion(UserScramCredentialAlteration):
    scram_credential_info: ScramCredentialInfo
    password: bytes
    salt: bytes | None

    def __init__(
        self, user: str, scram_credential_info: ScramCredentialInfo, password: bytes, salt: bytes | None = None
    ) -> None: ...

class UserScramCredentialDeletion(UserScramCredentialAlteration):
    mechanism: ScramMechanism

    def __init__(self, user: str, mechanism: ScramMechanism) -> None: ...
