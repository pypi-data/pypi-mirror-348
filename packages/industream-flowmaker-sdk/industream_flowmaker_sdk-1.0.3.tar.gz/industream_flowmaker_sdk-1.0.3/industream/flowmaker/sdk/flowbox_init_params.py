from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class FlowBoxInitParams:
    runtime_context: FlowRuntimeContext
    options: dict[str, Any]

    @staticmethod
    def from_dict(data: dict[str, Any]) -> FlowBoxInitParams:
        return FlowBoxInitParams(
            runtime_context=FlowRuntimeContext.from_dict(data["runtimeContext"]),
            options=data["options"]
        )


@dataclass
class FlowRuntimeContext:
    flowbox_id: str
    job_id: str
    node_id: str
    used_by: str | None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> FlowRuntimeContext:
        return FlowRuntimeContext(
            flowbox_id=data["flowBoxId"],
            job_id=data["jobId"],
            node_id=data["nodeId"],
            used_by=data.get("usedBy")
        )
