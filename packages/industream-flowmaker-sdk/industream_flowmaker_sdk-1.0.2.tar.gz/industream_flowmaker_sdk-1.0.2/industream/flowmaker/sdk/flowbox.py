from abc import ABC, abstractmethod
from collections.abc import Callable
from . import FlowBoxInitParams

class FlowBoxRaw(ABC):
    @abstractmethod
    def __init__(self, init_params: FlowBoxInitParams) -> None: ...


class FlowBoxSource(ABC):
    @abstractmethod
    def on_output_ready(self, output_name: str, header: bytes,
                        fn_ready_for_next_item: Callable[[bytes, bytes], None]) -> None: ...


class FlowBoxSink(ABC):
    @abstractmethod
    def on_input_received(self, input_name: str, header: bytes, data: bytes,
                          fn_ready_for_next_item: Callable[[], None]) -> None: ...


class FlowBoxDestroy(ABC):
    @abstractmethod
    def on_destroy(self) -> None: ...
