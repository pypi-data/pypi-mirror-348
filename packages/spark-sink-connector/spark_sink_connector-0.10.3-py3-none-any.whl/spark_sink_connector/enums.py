from enum import Enum, auto


class SchemaKind(Enum):
    AVRO = auto()
    PROTOBUF = auto()

class ConnectorOutputMode(str, Enum):
    APPEND = "append"
    OVERWRITE = "overwrite"
    UPSERT = "upsert"

class OpenTableFormat(str, Enum):
    HUDI = "hudi"
    DELTA = "delta"

class ConnectorMode(Enum):
    STREAM = auto()
    BATCH = auto()

class RunningMode(Enum):
    NORMAL = 'normal'
    OPTIMIZATION = 'optimization'
