from enum import IntEnum

class FlowMakerEvent(IntEnum):
    INIT_FLOW_BOX = 0x4026
    CURRENT_EVENT = 0x8200
    CAN_SEND_NEXT = 0x8001
    DESTROY_EVENT = 0x82FF
    HEARTBEAT_EVENT = 0x8210
    SCHEDULER_RESTART = 0x8220
