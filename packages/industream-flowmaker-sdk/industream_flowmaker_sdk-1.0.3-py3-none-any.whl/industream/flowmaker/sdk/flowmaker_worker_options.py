from __future__ import annotations
from dataclasses import dataclass
import os

class FlowMakerWorkerOptions:
    def __init__(self) -> None:
        self.worker_id = os.getenv("FM_WORKER_ID")
        self.worker_transport_adv_address = os.getenv("FM_WORKER_TRANSPORT_ADV_ADDRESS")
        self.router_transport_address = os.getenv("FM_ROUTER_TRANSPORT_ADDRESS")
        self.runtime_http_address = os.getenv("FM_RUNTIME_HTTP_ADDRESS")

    def to_immutable(self) -> FlowMakerImmutableWorkerOptions:
        if not self.worker_id or self.worker_id.isspace():
            raise ValueError("The 'FM_WORKER_ID' environment variable (or 'worker_id' option) is required.")
        
        if not self.worker_transport_adv_address or self.worker_transport_adv_address.isspace():
            raise ValueError("The 'FM_WORKER_TRANSPORT_ADV_ADDRESS' environment variable (or 'worker_transport_adv_address' option) is required.")
        
        if not self.router_transport_address or self.router_transport_address.isspace():
            raise ValueError("The 'FM_ROUTER_TRANSPORT_ADDRESS' environment variable (or 'router_transport_address' option) is required.")
        
        if not self.runtime_http_address or self.runtime_http_address.isspace():
            raise ValueError("The 'FM_RUNTIME_HTTP_ADDRESS' environment variable (or 'runtime_http_address' option) is required.")

        return FlowMakerImmutableWorkerOptions(
            self.worker_id,
            self.worker_transport_adv_address,
            self.router_transport_address,
            self.runtime_http_address
        )


@dataclass(frozen=True)
class FlowMakerImmutableWorkerOptions:
    worker_id: str
    worker_transport_adv_address: str
    router_transport_address: str
    runtime_http_address: str
