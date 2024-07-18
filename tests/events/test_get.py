from app.enums import EventType, OperationMode
from app.models import ElevatorEvent


def test_get_elevator_event(client, db):
    data = {
        "floor": 1,
        "target_floor": 5,
        "operation_mode": OperationMode.REGULAR.value,
        "number_of_passengers": 1,
        "type": EventType.MOVING.value,
        "temperature": 22,
    }
    event = ElevatorEvent(**data)
    db.session.add(event)
    db.session.commit()

    response = client.get(f"/api/v1/elevator-events/{event.id}")
    assert response.status_code == 200
    data = response.json
    assert data["id"] == event.id
    assert data["floor"] == event.floor
    assert data["target_floor"] == event.target_floor
    assert OperationMode.REGULAR == event.operation_mode
    assert data["number_of_passengers"] == event.number_of_passengers
    assert data["type"] == event.type.value


def test_list_elevator_events(client, db):
    events_data = [
        {
            "floor": 1,
            "target_floor": 5,
            "operation_mode": OperationMode.REGULAR.value,
            "type": EventType.MOVING.value,
            "temperature": 22,
        },
        {
            "floor": 2,
            "operation_mode": OperationMode.REGULAR.value,
            "type": EventType.RESTING.value,
            "temperature": 23,
        },
    ]
    for data in events_data:
        event = ElevatorEvent(**data)
        db.session.add(event)
    db.session.commit()

    response = client.get("/api/v1/elevator-events")
    assert response.status_code == 200
    events = response.json
    assert len(events) == len(events_data)

    # Assert each field for each event in events_data
    for i in range(len(events_data)):
        event = events[i]
        event_data = events_data[i]
        for attr in event_data.keys():
            assert event[attr] == event_data[attr]
