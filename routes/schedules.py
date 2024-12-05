from flask import Blueprint, jsonify, request
from utils.db_utils import get_db_connection

schedules_blueprint = Blueprint('schedules', __name__)


@schedules_blueprint.route('/schedules', methods=['POST'])
def create_schedule():
    data = request.json
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO schedule (subject_id, date, time, group_name) VALUES (%s, %s, %s, %s) RETURNING *;",
                    (data['subject_id'], data['date'], data['time'], data['group_name'])
                )
                conn.commit()
                new_schedule = cursor.fetchone()
        return jsonify(new_schedule), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@schedules_blueprint.route('/subjects/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_subject_by_id(id):
    if request.method == 'GET':
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM subject WHERE id = %s;", (id,))
                    subject = cursor.fetchone()
            if subject:
                return jsonify(subject), 200
            else:
                return jsonify({"error": "Subject not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'PUT':
        data = request.json
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE subject SET name = %s, professor_id = %s, credits = %s WHERE id = %s RETURNING *;",
                        (data['name'], data['professor_id'], data['credits'], id)
                    )
                    conn.commit()
                    updated_subject = cursor.fetchone()
            if updated_subject:
                return jsonify(updated_subject), 200
            else:
                return jsonify({"error": "Subject not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'DELETE':
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM subject WHERE id = %s RETURNING *;", (id,))
                    conn.commit()
                    deleted_subject = cursor.fetchone()
            if deleted_subject:
                return jsonify(deleted_subject), 200
            else:
                return jsonify({"error": "Subject not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@schedules_blueprint.route('/schedules/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_schedule_by_id(id):
    if request.method == 'GET':
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM schedule WHERE id = %s;", (id,))
                    schedule = cursor.fetchone()
                    if schedule and 'time' in schedule:
                        schedule['time'] = schedule['time'].strftime('%H:%M:%S')
            if schedule:
                return jsonify(schedule), 200
            else:
                return jsonify({"error": "Schedule not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'PUT':
        data = request.json
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE schedule SET subject_id = %s, date = %s, time = %s, group_name = %s WHERE id = %s RETURNING *;",
                        (data['subject_id'], data['date'], data['time'], data['group_name'], id)
                    )
                    conn.commit()
                    updated_schedule = cursor.fetchone()
                    if updated_schedule and 'time' in updated_schedule:
                        updated_schedule['time'] = updated_schedule['time'].strftime('%H:%M:%S')
            if updated_schedule:
                return jsonify(updated_schedule), 200
            else:
                return jsonify({"error": "Schedule not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'DELETE':
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM schedule WHERE id = %s RETURNING *;", (id,))
                    conn.commit()
                    deleted_schedule = cursor.fetchone()
            if deleted_schedule:
                return jsonify(deleted_schedule), 200
            else:
                return jsonify({"error": "Schedule not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Home route
@schedules_blueprint.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"}), 200