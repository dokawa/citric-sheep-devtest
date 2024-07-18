import pytest

from app.enums import EventType, OperationMode
from app.models import ElevatorEvent

MADE_UP_OPERATION_MODE = "made_up_operation_mode"
MADE_UP_EVENT_TYPE = "made_up_event_type"


@pytest.fixture
def elevator_event(db):
    event = ElevatorEvent(
        floor=1,
        target_floor=5,
        operation_mode=OperationMode.REGULAR.value,
        number_of_passengers=2,
        type=EventType.MOVING.value,
        temperature=22,
    )
    db.session.add(event)
    db.session.commit()
    return event


def test_update_floor(client, db, elevator_event):
    update_data = {
        "floor": 10,
    }

    response = client.put(
        f"/api/v1/elevator-events/{elevator_event.id}",
        json=update_data,
        content_type="application/json",
    )

    # Check the response
    assert response.status_code == 200
    assert response.json["message"] == "Updated successfully"

    # Verify the event was updated in the database
    updated_event = db.session.get(ElevatorEvent, elevator_event.id)
    assert updated_event.type == elevator_event.type
    assert updated_event.floor == 10
    assert updated_event.target_floor == elevator_event.target_floor
    assert updated_event.operation_mode == elevator_event.operation_mode
    assert updated_event.number_of_passengers == elevator_event.number_of_passengers
    assert updated_event.temperature == elevator_event.temperature


def test_update_operation_mode(client, db, elevator_event):
    update_data = {
        "operation_mode": OperationMode.OUT_OF_ORDER.value,
    }

    response = client.put(
        f"/api/v1/elevator-events/{elevator_event.id}",
        json=update_data,
        content_type="application/json",
    )

    # Check the response
    assert response.status_code == 200
    assert response.json["message"] == "Updated successfully"

    # Verify the event was updated in the database
    updated_event = db.session.get(ElevatorEvent, elevator_event.id)
    assert updated_event.type == elevator_event.type
    assert updated_event.floor == elevator_event.floor
    assert updated_event.target_floor == elevator_event.target_floor
    assert updated_event.operation_mode == OperationMode.OUT_OF_ORDER
    assert updated_event.number_of_passengers == elevator_event.number_of_passengers
    assert updated_event.temperature == elevator_event.temperature


def test_update_to_invalid_operation_mode(client, db, elevator_event):
    update_data = {
        "operation_mode": MADE_UP_OPERATION_MODE,
    }

    response = client.put(
        f"/api/v1/elevator-events/{elevator_event.id}",
        json=update_data,
        content_type="application/json",
    )

    # Check the response
    assert response.status_code == 400
    assert "Invalid value" in response.json["error"]


def test_update_number_of_passengers(client, db, elevator_event):
    update_data = {
        "number_of_passengers": 5,
    }

    response = client.put(
        f"/api/v1/elevator-events/{elevator_event.id}",
        json=update_data,
        content_type="application/json",
    )

    # Check the response
    assert response.status_code == 200
    assert response.json["message"] == "Updated successfully"

    # Verify the event was updated in the database
    updated_event = db.session.get(ElevatorEvent, elevator_event.id)
    assert updated_event.type == elevator_event.type
    assert updated_event.floor == elevator_event.floor
    assert updated_event.target_floor == elevator_event.target_floor
    assert updated_event.operation_mode == elevator_event.operation_mode
    assert updated_event.number_of_passengers == 5
    assert updated_event.temperature == elevator_event.temperature


def test_update_type(client, db, elevator_event):
    update_data = {
        "type": EventType.DEMAND.value,
    }

    response = client.put(
        f"/api/v1/elevator-events/{elevator_event.id}",
        json=update_data,
        content_type="application/json",
    )

    # Check the response
    assert response.status_code == 200
    assert response.json["message"] == "Updated successfully"

    # Verify the event was updated in the database
    updated_event = db.session.get(ElevatorEvent, elevator_event.id)
    assert updated_event.type == EventType.DEMAND
    assert updated_event.floor == elevator_event.floor
    assert updated_event.target_floor == elevator_event.target_floor
    assert updated_event.operation_mode == elevator_event.operation_mode
    assert updated_event.number_of_passengers == elevator_event.number_of_passengers
    assert updated_event.temperature == elevator_event.temperature


def test_update_to_invalid_type(client, db, elevator_event):
    update_data = {
        "type": MADE_UP_EVENT_TYPE,
    }

    response = client.put(
        f"/api/v1/elevator-events/{elevator_event.id}",
        json=update_data,
        content_type="application/json",
    )

    # Check the response
    assert response.status_code == 400
    assert "Invalid value" in response.json["error"]


def test_update_temperature(client, db, elevator_event):
    update_data = {
        "temperature": 25,
    }

    response = client.put(
        f"/api/v1/elevator-events/{elevator_event.id}",
        json=update_data,
        content_type="application/json",
    )

    # Check the response
    assert response.status_code == 200
    assert response.json["message"] == "Updated successfully"

    # Verify the event was updated in the database
    updated_event = db.session.get(ElevatorEvent, elevator_event.id)
    assert updated_event.type == elevator_event.type
    assert updated_event.floor == elevator_event.floor
    assert updated_event.target_floor == elevator_event.target_floor
    assert updated_event.operation_mode == elevator_event.operation_mode
    assert updated_event.number_of_passengers == elevator_event.number_of_passengers
    assert updated_event.temperature == 25


def test_update_movement_event_without_target_floor(client, db, elevator_event):
    update_data = {
        "target_floor": None,
    }

    response = client.put(
        f"/api/v1/elevator-events/{elevator_event.id}",
        json=update_data,
        content_type="application/json",
    )

    assert response.status_code == 400
    assert "Missing target_floor field for EventType" in response.json["error"]


def test_update_to_movement_event_without_target_floor(client, db):
    data = {
        "floor": 5,
        "operation_mode": OperationMode.REGULAR.value,
        "number_of_passengers": 3,
        "type": EventType.RESTING.value,
    }

    event = ElevatorEvent(**data)
    db.session.add(event)
    db.session.commit()

    update_data = {
        "type": EventType.MOVING.value,
    }

    response = client.put(
        f"/api/v1/elevator-events/{event.id}",
        json=update_data,
        content_type="application/json",
    )

    assert response.status_code == 400
    assert "Missing target_floor field for EventType" in response.json["error"]
