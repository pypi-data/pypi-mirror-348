from __future__ import annotations
from collections.abc import Callable
from typing import Any
from . import FlowBoxRegistrationInfo, FlowBoxRaw

def flowbox(registration_info: FlowBoxRegistrationInfo) -> Callable[[Any], Any]:
    def decorator(cls: Any) -> Any:
        cls.registration_info = registration_info
        return cls

    return decorator


def get_registration_info(flowbox_type: type[FlowBoxRaw]) -> FlowBoxRegistrationInfo:
    if not hasattr(flowbox_type, "registration_info"):
        raise AttributeError(f"Missing registration info for the {flowbox_type.__name__} box. Please add a @flowbox() decorator to the {flowbox_type.__name__} class.")

    if not isinstance(flowbox_type.registration_info, FlowBoxRegistrationInfo):
        raise TypeError(f"Invalid registration info type for the {flowbox_type.__name__} box.")

    return flowbox_type.registration_info
