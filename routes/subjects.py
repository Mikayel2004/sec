# /routes/subjects.py


from flask import Blueprint, jsonify, request
from utils.db_utils import get_db_connection

# Define the blueprint
subjects_blueprint = Blueprint('subjects', __name__)


# CRUD Operations for Subjects
@subjects_blueprint.route('/', methods=['GET', 'POST'])
def handle_subjects():
    if request.method == 'GET':
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM subject;")
                    subjects = cursor.fetchall()
            return jsonify(subjects), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'POST':
        data = request.json
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO subject (name, hours, professor_id) VALUES (%s, %s, %s) RETURNING *;",
                        (data['name'], data['hours'], data['professor_id'])
                    )
                    conn.commit()
                    new_subject = cursor.fetchone()
            return jsonify(new_subject), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@subjects_blueprint.route('/', methods=['GET', 'PUT', 'DELETE'])
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
                        "UPDATE subject SET name = %s, hours = %s, professor_id = %s WHERE id = %s RETURNING *;",
                        (data['name'], data['hours'], data['professor_id'], id)
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

@subjects_blueprint.route('/with_professors', methods=['GET'])
def get_subjects_with_professors():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT subject.name AS subject_name, professor.name AS professor_name
                    FROM subject
                    INNER JOIN professor ON subject.professor_id = professor.id;
                """
                cursor.execute(query)
                results = cursor.fetchall()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching subjects with professors: {str(e)}"}), 500

@subjects_blueprint.route('/group_by_hours', methods=['GET'])
def group_subjects_by_hours():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT hours, COUNT(*) AS subject_count
                    FROM subject
                    GROUP BY hours
                    ORDER BY hours;
                """
                cursor.execute(query)
                results = cursor.fetchall()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": f"Error grouping subjects by hours: {str(e)}"}), 500
