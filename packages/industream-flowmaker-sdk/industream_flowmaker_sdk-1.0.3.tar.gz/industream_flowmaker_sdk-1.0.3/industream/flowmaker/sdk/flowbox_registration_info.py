from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any

class FlowBoxType(IntEnum):
    SOURCE = 1
    SINK = 2
    PIPE = 3


class SerializationFormat(IntEnum):
    MSGPACK = 1
    JSON = 2


@dataclass(frozen=True)
class FlowBoxIOInterfaces:
    inputs: list[FlowBoxIO] = field(default_factory=list)
    outputs: list[FlowBoxIO] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "inputs": [i.to_dict() for i in self.inputs],
            "outputs": [o.to_dict() for o in self.outputs],
        }


@dataclass(frozen=True)
class FlowBoxIO:
    name: str
    display_name: str
    supported_formats: list[SerializationFormat] = field(default_factory=lambda: [SerializationFormat.MSGPACK])

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "displayName": self.display_name,
            "supportedFormats": [f.name.lower() for f in self.supported_formats]
        }


@dataclass(frozen=True)
class FlowBoxUIConfig:
    default_options: dict[str, Any] | None = None
    implementation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "defaultOptions": self.default_options,
            "implementation": self.implementation
        }


@dataclass(frozen=True)
class FlowBoxRegistrationInfo:
    id: str
    display_name: str
    current_version: str
    type: FlowBoxType
    icon: str
    stateless: bool = False
    io_interfaces: FlowBoxIOInterfaces = FlowBoxIOInterfaces()
    ui_config: FlowBoxUIConfig = FlowBoxUIConfig()

    def to_dict(self, agent: str, worker_id: str, worker_data_connection_string: str) -> dict[str, Any]:
        return {
            "id": self.id,
            "displayName": self.display_name,
            "currentVersion": self.current_version,
            "type": self.type.name.lower(),
            "icon": self.icon,
            "stateless": self.stateless,
            "agent": agent,
            "workerId": worker_id,
            "workerDataConnectionString": worker_data_connection_string,
            "ioInterfaces": self.io_interfaces.to_dict(),
            "uiConfig": self.ui_config.to_dict()
        }
