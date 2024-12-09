# /routes/professors.py

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


@professors_blueprint.route('/search', methods=['GET'])
def search_professors():
    # Get the search query parameter
    query = request.args.get('query', '')  # Default to empty string if no query provided

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Search in the 'name', 'degree', and 'department' fields
                cursor.execute("""
                    SELECT * FROM professor
                    WHERE name ILIKE %s OR degree ILIKE %s OR department ILIKE %s;
                """, (f'%{query}%', f'%{query}%', f'%{query}%'))
                results = cursor.fetchall()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": f"Error performing search: {str(e)}"}), 500



@professors_blueprint.route('/sorted', methods=['GET'])
def get_sorted_professors():
    sort_field = request.args.get('sort_field', 'name')
    sort_order = request.args.get('sort_order', 'ASC')

    if sort_field not in ['name', 'department']:
        return jsonify({"error": "Invalid sort field"}), 400
    if sort_order.upper() not in ['ASC', 'DESC']:
        return jsonify({"error": "Invalid sort order"}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = f"""
                    SELECT * FROM professor
                    ORDER BY {sort_field} {sort_order};
                """
                cursor.execute(query)
                professors = cursor.fetchall()
        return jsonify(professors), 200
    except Exception as e:
        return jsonify({"error": f"Error sorting professors: {str(e)}"}), 500

@professors_blueprint.route('/filter', methods=['GET'])
def filter_professors():
    degree = request.args.get('degree')
    department = request.args.get('department')

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT * FROM professor
                    WHERE degree = %s AND department = %s;
                """
                cursor.execute(query, (degree, department))
                professors = cursor.fetchall()
        return jsonify(professors), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching filtered professors: {str(e)}"}), 500


@professors_blueprint.route('/populate_metadata', methods=['POST'])
def populate_metadata():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE professor
                    SET metadata = jsonb_build_object(
                        'bio', 'This professor specializes in machine learning and AI.',
                        'achievements', ARRAY['Published 10 papers', 'Supervised 5 PhD students'],
                        'interests', ARRAY['AI', 'ML', 'Big Data']
                    )
                    WHERE metadata IS NULL;
                """)
                conn.commit()
        return jsonify({"message": "Metadata populated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Error populating metadata: {str(e)}"}), 500

@professors_blueprint.route('/search_metadata', methods=['GET'])
def search_metadata():
    search_pattern = request.args.get('pattern', '')

    if not search_pattern:
        return jsonify({"error": "Search pattern is required"}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT id, name, metadata
                    FROM professor
                    WHERE metadata::TEXT ~* %s;
                """
                cursor.execute(query, (search_pattern,))
                results = cursor.fetchall()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": f"Error performing metadata search: {str(e)}"}), 500


@professors_blueprint.route('/paginated', methods=['GET'])
def get_paginated_professors():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))
        offset = (page - 1) * per_page

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM professor;")
                total_records = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT * FROM professor ORDER BY id LIMIT %s OFFSET %s;",
                    (per_page, offset)
                )
                professors = cursor.fetchall()

        return jsonify({
            "total": total_records,
            "page": page,
            "per_page": per_page,
            "data": professors
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error during pagination: {str(e)}"}), 500
