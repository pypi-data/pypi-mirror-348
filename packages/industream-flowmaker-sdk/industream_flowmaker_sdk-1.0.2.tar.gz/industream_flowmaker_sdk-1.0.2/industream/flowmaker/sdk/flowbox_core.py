import asyncio
from abc import abstractmethod
from collections.abc import Callable
from reactivex import zip
from reactivex.subject import Subject
from . import FlowBoxRaw, FlowBoxSink, FlowBoxSource, FlowBoxInitParams

class FlowBoxCore(FlowBoxRaw, FlowBoxSink, FlowBoxSource):
    def __init__(self, init_params: FlowBoxInitParams) -> None:
        self._output_synchronizers: dict[str, OutputSynchronizer] = {}

    @abstractmethod
    async def on_input(self, input_name: str, header: bytes, data: bytes) -> None: ...

    def on_input_received(self, input_name: str, header: bytes, data: bytes,
                          fn_ready_for_next_item: Callable[[], None]) -> None:
        asyncio.create_task(self.on_input(input_name, header, data)) \
            .add_done_callback(lambda _: fn_ready_for_next_item())


    def on_output_ready(self, output_name: str, header: bytes,
                        fn_ready_for_next_item: Callable[[bytes, bytes], None]) -> None:
        output_synchronizer = (self._output_synchronizers.get(output_name) or OutputSynchronizer())
        self._output_synchronizers[output_name] = output_synchronizer

        output_synchronizer.output_ready_subject.on_next(fn_ready_for_next_item)

    async def push(self, output_name: str, header: bytes, data: bytes, output_buffer_size: int = 0):
        future = asyncio.get_running_loop().create_future()

        output_synchronizer = (self._output_synchronizers.get(output_name) or OutputSynchronizer())
        self._output_synchronizers[output_name] = output_synchronizer

        if output_synchronizer.msg_count_in_buffer < output_buffer_size:
            future.set_result(None)

        output_synchronizer.msg_count_in_buffer += 1
        output_synchronizer.push_subject.on_next((header, data, lambda: future.set_result(None) if not future.done() else None))

        await future


class OutputSynchronizer:
    """Synchronize pushed data with the "on output ready" event."""

    def __init__(self) -> None:
        self.msg_count_in_buffer = 0
        self.push_subject: Subject[tuple[bytes, bytes, Callable[[], None]]] = Subject()
        self.output_ready_subject: Subject[Callable[[bytes, bytes], None]] = Subject()

        zip(self.push_subject, self.output_ready_subject) \
            .subscribe(lambda pair: self._on_next(*pair))

    def _on_next(self, push_info: tuple, fn_ready_for_next_item: Callable):
        data_to_push, header_to_push, complete_push = push_info

        self.msg_count_in_buffer -= 1
        fn_ready_for_next_item(data_to_push, header_to_push)
        complete_push()
