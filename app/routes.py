from enum import Enum

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app.core import db
from app.models import ElevatorEvent

main = Blueprint("main", __name__)


@main.route("/api/v1/elevator-events", methods=["POST"])
def create_elevator_event():
    try:
        data = request.json
        new_event = ElevatorEvent(**data)

        db.session.add(new_event)
        db.session.commit()
        return jsonify({"message": "Created successfully", "id": new_event.id}), 201
    except KeyError as e:
        db.session.rollback()
        return jsonify({"error": f"Missing key: {e}"}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": f"{e}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


@main.route("/api/v1/elevator-events/<int:event_id>", methods=["GET"])
def get_elevator_event(event_id):
    event = db.session.get(ElevatorEvent, event_id)
    if event:
        # Create a dictionary to hold the event data
        event_data = {
            column.name: getattr(event, column.name)
            for column in ElevatorEvent.__table__.columns
        }

        # Handle enum values specifically if needed
        for key, value in event_data.items():
            if isinstance(value, Enum):
                event_data[key] = value.value

        return jsonify(event_data), 200
    else:
        return jsonify({"message": "Event not found"}), 404


@main.route("/api/v1/elevator-events", methods=["GET"])
def list_elevator_events():
    events = ElevatorEvent.query.all()
    event_list = []
    for event in events:
        # Create a dictionary to hold the event data
        event_data = {
            column.name: getattr(event, column.name)
            for column in ElevatorEvent.__table__.columns
        }

        # Handle enum values specifically if needed
        for key, value in event_data.items():
            if isinstance(value, Enum):
                event_data[key] = value.value
        event_list.append(event_data)
    return jsonify(event_list), 200


@main.route("/api/v1/elevator-events/<int:event_id>", methods=["PUT"])
def update_elevator_event(event_id):
    try:
        data = request.json
        event = db.session.get(ElevatorEvent, event_id)
        if event:
            for key, value in data.items():
                if hasattr(event, key):
                    setattr(event, key, value)
            db.session.commit()
            return jsonify({"message": "Updated successfully"}), 200
        else:
            return jsonify({"message": "Event not found"}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except KeyError as e:
        db.session.rollback()
        return jsonify({"error": f"Missing key: {e}"}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": f"{e}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


@main.route("/api/v1/elevator-events/delete-all", methods=["DELETE"])
def delete_all_elevator_events():
    try:
        # Delete all records
        num_deleted = db.session.query(ElevatorEvent).delete()
        db.session.commit()
        return jsonify({"message": f"Deleted {num_deleted} records successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete records", "details": str(e)}), 500


@main.route("/api/v1/elevator-events/<int:event_id>", methods=["DELETE"])
def delete_elevator_event(event_id):
    event = db.session.get(ElevatorEvent, event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Deleted successfully"}), 200
    else:
        return jsonify({"message": "Event not found"}), 404
