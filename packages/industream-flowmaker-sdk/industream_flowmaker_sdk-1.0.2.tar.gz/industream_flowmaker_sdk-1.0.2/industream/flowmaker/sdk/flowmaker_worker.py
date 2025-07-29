import asyncio
import httpx
import msgpack
import zmq
import zmq.asyncio
from typing import Any
from .flowbox_decorator import get_registration_info
from . import (
    FlowBoxRaw,
    FlowBoxSource,
    FlowBoxSink,
    FlowBoxDestroy,
    FlowBoxInitParams,
    FlowMakerEvent,
    FlowMakerImmutableWorkerOptions
)

class FlowMakerWorker:
    ACK_HEADER = (0x9000).to_bytes(8, byteorder="little")
    ERROR_HEADER = (0xFFFF).to_bytes(8, byteorder="little")

    def __init__(self, options: FlowMakerImmutableWorkerOptions, implementations: dict[str, type[FlowBoxRaw]]) -> None:
        self._options = options
        self._implementations = implementations
        self._flowbox_instances: dict[str, FlowBoxRaw] = {}
        self._socket = zmq.asyncio.Context().socket(zmq.SocketType.ROUTER)

    async def run(self):
        http_client = httpx.AsyncClient(base_url=self._options.runtime_http_address)

        # Register all declared Flow boxes.
        await self._register(http_client)

        self._socket.bind(self._options.router_transport_address)
        await self._listen_incoming_messages()


    async def _register(self, http_client: httpx.AsyncClient) -> None:
        registrations = [get_registration_info(impl) for impl in self._implementations.values()]
        register_request = [
            registration.to_dict(
                "flowmaker-python-sdk/1.0.1;os=linux;tag=docker", # TODO: build this agent string using environment info
                self._options.worker_id, self._options.worker_transport_adv_address)
            for registration in registrations
        ]
        result = await http_client.post("/workers/register", json=register_request)
        result.raise_for_status()

        flowbow_ids = [f'"{r.id}"' for r in registrations]
        print(f"Worker started with {', '.join(flowbow_ids)} registered.")


    async def _listen_incoming_messages(self) -> None:
        while True:
            msg_parts = await self._socket.recv_multipart()

            # Caution: keep the processing of each message in a separate function, to maintain
            # a local scope of variables (since Python doesn't enforce local scope in while/for loops).
            await self._process_incoming_message(msg_parts)

    async def _process_incoming_message(self, msg_parts: list[bytes]) -> None:
        if len(msg_parts) < 6:
            print("Invalid message received: it must contain at least 6 parts.")
            return

        routing_id, token, encoded_node_ref, encoded_io_name, header, data, *_ = msg_parts

        node_ref = encoded_node_ref.decode()
        io_name = encoded_io_name.decode()
        event_id = int.from_bytes(header[:4], byteorder="little")

        if event_id == FlowMakerEvent.HEARTBEAT_EVENT:
            # print("HEARTBEAT_EVENT received")
            # Acknowledge to indicate that the worker is still alive.
            await self._socket.send_multipart([routing_id, token, self.ACK_HEADER])

        elif event_id == FlowMakerEvent.INIT_FLOW_BOX:
            # print("INIT_FLOW_BOX received")
            msg = msgpack.unpackb(data)
            init_params = FlowBoxInitParams.from_dict(msg)

            implementation = self._implementations[init_params.runtime_context.flowbox_id]
            self._flowbox_instances[node_ref] = implementation(init_params)

            print(f"Flow box {node_ref} initialized.")
            await self._socket.send_multipart([routing_id, token, self.ACK_HEADER])

        elif event_id == FlowMakerEvent.CURRENT_EVENT:
            # print("CURRENT_EVENT received")
            flowbox_instance = await self._get_flowbox_instance(routing_id, token, node_ref)
            if flowbox_instance is None:
                return

            if isinstance(flowbox_instance, FlowBoxSink):
                flowbox_instance.on_input_received(
                    io_name, header, data,
                    lambda: self._send_multipart_and_forget([routing_id, token, self.ACK_HEADER]))
            else:
                print(f"Flow box {node_ref} does not implement FlowBoxSink.")

        elif event_id == FlowMakerEvent.CAN_SEND_NEXT:
            # print("CAN_SEND_NEXT received")
            flowbox_instance = await self._get_flowbox_instance(routing_id, token, node_ref)
            if flowbox_instance is None:
                return

            if isinstance(flowbox_instance, FlowBoxSource):
                flowbox_instance.on_output_ready(
                    io_name, header,
                    lambda header, data: self._send_multipart_and_forget([routing_id, token, header, data]))
            else:
                print(f"Flow box {node_ref} does not implement FlowBoxSource.")

        elif event_id == FlowMakerEvent.DESTROY_EVENT:
            # print("DESTROY_EVENT received")
            flowbox_instance = await self._get_flowbox_instance(routing_id, token, node_ref)
            if flowbox_instance is None:
                return

            if isinstance(flowbox_instance, FlowBoxDestroy):
                flowbox_instance.on_destroy()
            self._flowbox_instances.pop(node_ref)

            print(f"Flow box {node_ref} destroyed.")
            await self._socket.send_multipart([routing_id, token, self.ACK_HEADER])

        elif event_id == FlowMakerEvent.SCHEDULER_RESTART:
            # print("SCHEDULER_RESTART received")
            for flowbox_instance in self._flowbox_instances.values():
                if isinstance(flowbox_instance, FlowBoxDestroy):
                    flowbox_instance.on_destroy()
            self._flowbox_instances.clear()

            print("Scheduler restarted! All Flow box instances have just been destroyed.")
            await self._socket.send_multipart([routing_id, token, self.ACK_HEADER])


    async def _get_flowbox_instance(self, routing_id: bytes, token: bytes, node_ref: str) -> FlowBoxRaw | None:
        flowbox_instance = self._flowbox_instances.get(node_ref)
        if flowbox_instance is None:
            await self._socket.send_multipart([routing_id, token, self.ERROR_HEADER])
            print(f"Flow box {node_ref} not found or deleted.")

        return flowbox_instance

    def _send_multipart_and_forget(self, msg_parts: Any) -> None:
        asyncio.ensure_future(self._socket.send_multipart(msg_parts)) # Fire and forget
