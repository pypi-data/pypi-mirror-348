from __future__ import annotations
from collections.abc import Callable
from . import FlowMakerWorkerOptions, FlowMakerWorker, FlowBoxRaw
from .flowbox_decorator import get_registration_info

class FlowMakerWorkerBuilder:
    def __init__(self) -> None:
        self._options = FlowMakerWorkerOptions()
        self._implementations: dict[str, type[FlowBoxRaw]] = {}

    def configure(self, configureOptions: Callable[[FlowMakerWorkerOptions], None]) -> FlowMakerWorkerBuilder:
        configureOptions(self._options)
        return self

    def declare_flowbox(self, flowbox_type: type[FlowBoxRaw]) -> FlowMakerWorkerBuilder:
        registration_info = get_registration_info(flowbox_type)
        id = f"{registration_info.id}/{registration_info.current_version}"
        self._implementations[id] = flowbox_type
        return self

    def build(self) -> FlowMakerWorker:
        immutable_options = self._options.to_immutable()
        return FlowMakerWorker(immutable_options, self._implementations)
