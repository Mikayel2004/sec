from flask import Blueprint, jsonify, request, render_template
from utils.db_utils import get_db_connection

professors_blueprint = Blueprint('professors', __name__)

@professors_blueprint.route('/', methods=['GET'])
def handle_professors():
    if request.method == 'GET':
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM professor;")
                    professors = cursor.fetchall()
            return jsonify(professors), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred while fetching professors: {str(e)}"}), 500
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        required_fields = ['name', 'degree', 'department', 'position']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO professor (name, degree, department, position) VALUES (%s, %s, %s, %s) RETURNING *;",
                        (data['name'], data['degree'], data['department'], data['position'])
                    )
                    conn.commit()
                    new_professor = cursor.fetchone()
            return jsonify(new_professor), 201
        except Exception as e:
            return jsonify({"error": f"An error occurred while adding professor: {str(e)}"}), 500


@professors_blueprint.route('/', methods=['GET', 'PUT', 'DELETE'])
def handle_professor_by_id(id):
    if request.method == 'GET':
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM professor WHERE id = %s;", (id,))
                    professor = cursor.fetchone()
            if professor:
                return jsonify(professor), 200
            else:
                return jsonify({"error": f"Professor with ID {id} not found"}), 404
        except Exception as e:
            return jsonify({"error": f"An error occurred while fetching professor: {str(e)}"}), 500
    
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        required_fields = ['name', 'degree', 'department', 'position']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE professor SET name = %s, degree = %s, department = %s, position = %s WHERE id = %s RETURNING *;",
                        (data['name'], data['degree'], data['department'], data['position'], id)
                    )
                    conn.commit()
                    updated_professor = cursor.fetchone()
            if updated_professor:
                return jsonify(updated_professor), 200
            else:
                return jsonify({"error": f"Professor with ID {id} not found"}), 404
        except Exception as e:
            return jsonify({"error": f"An error occurred while updating professor: {str(e)}"}), 500
    
    elif request.method == 'DELETE':
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM professor WHERE id = %s RETURNING *;", (id,))
                    conn.commit()
                    deleted_professor = cursor.fetchone()
            if deleted_professor:
                return jsonify(deleted_professor), 200
            else:
                return jsonify({"error": f"Professor with ID {id} not found"}), 404
        except Exception as e:
            return jsonify({"error": f"An error occurred while deleting professor: {str(e)}"}), 500
