from app.enums import EventType, OperationMode
from app.models import ElevatorEvent


def test_delete_elevator_event(client, db):
    event = ElevatorEvent(
        floor=1,
        target_floor=5,
        operation_mode=OperationMode.REGULAR.value,
        number_of_passengers=1,
        type=EventType.MOVING.value,
    )
    db.session.add(event)
    db.session.commit()

    response = client.delete(f"/api/v1/elevator-events/{event.id}")
    assert response.status_code == 200

    # Verify the event was deleted
    deleted_event = db.session.get(ElevatorEvent, event.id)
    assert deleted_event is None


def test_delete_all_elevator_events(client, db):
    """Test deleting all ElevatorEvents."""
    events_data = [
        {
            "floor": 1,
            "operation_mode": OperationMode.REGULAR.value,
            "number_of_passengers": 1,
            "type": EventType.RESTING.value,
        },
        {
            "floor": 2,
            "operation_mode": OperationMode.REGULAR.value,
            "number_of_passengers": 2,
            "type": EventType.RESTING.value,
        },
    ]
    for data in events_data:
        event = ElevatorEvent(**data)
        db.session.add(event)
    db.session.commit()

    assert ElevatorEvent.query.count() == 2

    response = client.delete("/api/v1/elevator-events/delete-all")
    assert response.status_code == 200
    assert response.json["message"] == "Deleted 2 records successfully"
    assert ElevatorEvent.query.count() == 0
