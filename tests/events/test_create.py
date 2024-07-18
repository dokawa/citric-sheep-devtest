from app.enums import EventType, OperationMode
from app.models import ElevatorEvent

MADE_UP_OPERATION_MODE = "made_up_operation_mode"
MADE_UP_EVENT_TYPE = "made_up_event_type"


def test_create_elevator_event(client, db):
    data = {
        "floor": 5,
        "target_floor": 0,
        "operation_mode": OperationMode.REGULAR.value,
        "number_of_passengers": 3,
        "type": EventType.RESTING.value,
    }
    response = client.post("/api/v1/elevator-events", json=data)
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["message"] == "Created successfully"

    event = ElevatorEvent.query.first()
    assert event is not None
    assert event.floor == data["floor"]
    assert event.operation_mode == OperationMode.REGULAR
    assert event.number_of_passengers == data["number_of_passengers"]
    assert event.type.value == data["type"]


def test_create_invalid_operation_mode(client):
    data = {
        "floor": 5,
        "operation_mode": MADE_UP_OPERATION_MODE,
        "number_of_passengers": 3,
        "type": EventType.RESTING.value,
    }

    response = client.post("/api/v1/elevator-events", json=data)
    assert response.status_code == 400
    assert "Invalid" in response.json["error"]


def test_create_invalid_event_type(client):
    data = {
        "floor": 5,
        "operation_mode": OperationMode.REGULAR.value,
        "number_of_passengers": 3,
        "type": MADE_UP_EVENT_TYPE,
    }
    response = client.post("/api/v1/elevator-events", json=data)

    assert response.status_code == 400
    assert "Invalid" in response.json["error"]


def test_create_invalid_movement_event(client):
    data = {
        "floor": 5,
        "operation_mode": OperationMode.REGULAR.value,
        "number_of_passengers": 3,
        "type": EventType.MOVING.value,
    }
    response = client.post("/api/v1/elevator-events", json=data)

    assert response.status_code == 400
    assert "Missing target_floor field for EventType: moving" in response.json["error"]
