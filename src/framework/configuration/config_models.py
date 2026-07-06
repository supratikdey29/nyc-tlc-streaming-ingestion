from pydantic import BaseModel,Field


class DatasetConfig(BaseModel):
    name: str


class SourceConfig(BaseModel):
    type: str
    path: str
    format: str
    file_pattern: str


class TargetConfig(BaseModel):
    catalog: str
    schema_name: str = Field(alias="schema")
    table: str


class StreamingConfig(BaseModel):
    enabled: bool
    trigger: str
    mode: str


class CheckpointConfig(BaseModel):
    path: str


class SchemaConfig(BaseModel):
    mode: str
    location:str


class AuditConfig(BaseModel):
    enabled: bool


class PipelineConfig(BaseModel):
    dataset: DatasetConfig
    source: SourceConfig
    target: TargetConfig
    streaming: StreamingConfig
    checkpoint: CheckpointConfig
    schema_settings: SchemaConfig = Field(alias="schema")
    audit: AuditConfig