from flask import Blueprint, request, jsonify
from mysql.connector import Error
from datetime import date

# Go up one directory to import from database
import sys
sys.path.append('..')
from database.connection import get_db_connection

member_bp = Blueprint('member_bp', __name__)

# --- Helper Functions ---
def fetch_all_members_from_db():
    """Fetch all members from the database."""
    conn = get_db_connection()
    if not conn:
        return None,"Database connection failed"
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Members ORDER BY name ASC")
        members = cursor.fetchall()
        return members, None
    except Error as e:
        return None, f"Error fetching members: {e}"
    finally:
        cursor.close()
        conn.close()

# --- API ROUTES ---

@member_bp.route('/', methods=['GET'])
def get_all_members():
    "API endpoint to get a list of all members."
    members, error = fetch_all_members_from_db()
    if error:
        return jsonify({"error": error}), 500
    return jsonify(members), 200

@member_bp.route('/add', methods=['POST'])
def add_member():
    """API endpoint to add a new member."""
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email') or not  data.get('membership_plan'):
        return jsonify({"error": "Missing required fields: name, email, or membership_plan"}), 400

    name = data['name']
    email = data['email']
    phone_number = data.get('phone_number', '')
    membership_plan = data['membership_plan']
    join_date = date.today().strftime('%Y-%m-%d')

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    try:
        # Check for duplicate email

        cursor.execute("SELECT email FROM Members WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "A member with this email already exists"}), 409
        cursor.execute(
            "INSERT INTO Members (name, email, phone_number, membership_plan, join_date) VALUES (%s, %s, %s, %s, %s)",
            (name, email, phone_number, membership_plan, join_date)
        )
        conn.commit()

        #  Return the newly created member's data
        member_id = cursor.lastrowid
        return jsonify({
            "message": "Member added successfully",
            "member_id" : member_id,
            }), 201
    
    except Error as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


@member_bp.route('/update/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """API endpoint to update an existing member."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400

    # Building the query dynamically based on provided fields
    fields_to_update = []
    values = []
    for key, value in data.items():
        # Ensure only valid columns are updated
        if key in ['name', 'email', 'phone_number', 'membership_plan', 'status']:
            fields_to_update.append(f"{key} = %s")
            values.append(value)

    if not fields_to_update:
        return jsonify({"error": "No valid fields to update"}), 400

    values.append(member_id) # For the WHERE clause
    query = f"UPDATE Members SET {', '.join(fields_to_update)} WHERE member_id = %s"

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(query, tuple(values))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Member not found or no new data to update"}), 404

        return jsonify({"message": f"Member with ID {member_id} updated successfully."}), 200

    except Error as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


@member_bp.route('/delete/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """API endpoint to delete a member."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Members WHERE member_id = %s", (member_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Member not found"}), 404

        return jsonify({"message": f"Member with ID {member_id} deleted successfully."}), 200

    except Error as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@member_bp.route('/stats',methods=['GET'])
def get_member_stats():
    """API endpoint to get member statistics."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    stats={}

    try:
        # 1. Get total member count
        cursor.execute("SELECT COUNT(member_id) AS total_members FROM Members")
        total_results = cursor.fetchone()
        stats['total_members'] = total_results['total_members'] if total_results else 0

        # 2. Get count of active members
        cursor.execute("SELECT COUNT(member_id) AS active_members FROM Members WHERE status = 'active'")
        active_results = cursor.fetchone()
        stats['active_members'] = active_results['active_members'] if active_results else 0

        # 3. Get member count by plan
        cursor.execute("SELECT membership_plan,COUNT(member_id) AS count FROM Members Group by membership_plan")
        plan_counts = cursor.fetchall()
        stats['plan_distribution'] = {item['membership_plan']: item['count'] for item in plan_counts} # type: ignore

        return jsonify(stats), 200

    except Error as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
    finally:
        cursor.close()
        conn.close()
