from datetime import UTC, datetime

from sqlalchemy import event
from sqlalchemy.orm import validates

from app.core import db
from app.enums import EventType, OperationMode


class ElevatorEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(UTC))
    floor = db.Column(db.Integer, nullable=False)
    target_floor = db.Column(db.Integer, nullable=True)
    operation_mode = db.Column(
        db.Enum(OperationMode, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    )
    number_of_passengers = db.Column(
        db.Integer, nullable=True
    )  # could be used to prioritize floors with more passengers
    type = db.Column(
        db.Enum(EventType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    )
    temperature = db.Column(db.Float, nullable=True)

    @validates("type", "operation_mode")
    def validate_field(self, key, value):

        if value and key == "type":
            values = {t.value for t in EventType}
            if value not in values:
                raise ValueError(f"Invalid value for type: {key}:{value}")

        if value and key == "operation_mode":
            values = {t.value for t in OperationMode}
            if value not in values:
                raise ValueError(f"Invalid value for type: {key}:{value}")

        return value


def validate_create_moving_event(mapper, connection, target):
    if target.type == EventType.MOVING.value and not target.target_floor:
        raise ValueError(f"Missing target_floor field for EventType: {target.type}")


def validate_update_moving_event(mapper, connection, target):
    if (
        target.type
        == EventType.MOVING  # when it is an update it has the enum value already
        or target.type
        == EventType.MOVING.value  # when it is a create it receives the string value
    ) and not target.target_floor:
        raise ValueError(f"Missing target_floor field for EventType: {target.type}")


event.listen(ElevatorEvent, "before_insert", validate_create_moving_event)
event.listen(ElevatorEvent, "before_update", validate_update_moving_event)
