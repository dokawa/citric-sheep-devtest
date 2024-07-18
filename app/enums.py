from enum import Enum


class OperationMode(Enum):
    REGULAR = "regular"
    OUT_OF_ORDER = "out_of_order"
    SPECIAL = "special"  # includes emergency and special modes


class EventType(Enum):
    DEMAND = "demand"
    MOVING = "moving"
    RESTING = "resting"
