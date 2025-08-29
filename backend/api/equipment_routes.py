from flask import Blueprint, request, jsonify
from .auth_routes import token_required
from .equipment import Equipment

# Create a Blueprint for equipment-related routes
equipment_bp = Blueprint('equipment_bp', __name__)

@equipment_bp.route('/', methods=['GET'])
@token_required
def get_all_equipment(current_user):
    """API endpoint to get a list of all equipment."""
    # Any authenticated user (admin, employee, or member) can view equipment
    all_equipment = Equipment.get_all()
    
    # Convert the list of Equipment objects into a list of dictionaries
    equipment_list = [eq.__dict__ for eq in all_equipment]
    
    return jsonify(equipment_list), 200

@equipment_bp.route('/<int:equipment_id>', methods=['GET'])
@token_required
def get_equipment_by_id(current_user, equipment_id):
    """API endpoint to get a single piece of equipment by its ID."""
    equipment = Equipment.find_by_id(equipment_id)
    if equipment:
        return jsonify(equipment.__dict__), 200
    else:
        return jsonify({"error": "Equipment not found"}), 404

@equipment_bp.route('/add', methods=['POST'])
@token_required
def add_equipment(current_user):
    """API endpoint to add a new piece of equipment."""
    # Security check: Only admins or employees can add equipment
    if current_user.get('role') not in ['admin', 'IT', 'Trainer']:
        return jsonify({"error": "Unauthorized: Only admins or employees can add equipment"}), 403

    data = request.get_json()
    required_fields = ['e_name', 'e_qty', 'e_unit_price', 'e_category']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_equipment = Equipment.create(**data)

    if new_equipment:
        return jsonify({
            "message": "Equipment added successfully",
            "equipment": new_equipment.__dict__
        }), 201
    else:
        return jsonify({"error": "Failed to add equipment"}), 500

@equipment_bp.route('/<int:equipment_id>', methods=['PUT'])
@token_required
def update_equipment(current_user, equipment_id):
    """API endpoint to update an existing piece of equipment."""
    if current_user.get('role') not in ['admin', 'IT', 'Trainer']:
        return jsonify({"error": "Unauthorized: Only admins or employees can update equipment"}), 403
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    updated_equipment = Equipment.update(equipment_id, data)
    
    if updated_equipment:
        return jsonify({"message": "Equipment updated successfully", "equipment": updated_equipment.__dict__}), 200
    else:
        return jsonify({"error": "Equipment not found or update failed"}), 404

@equipment_bp.route('/<int:equipment_id>', methods=['DELETE'])
@token_required
def delete_equipment(current_user, equipment_id):
    """API endpoint to delete a piece of equipment."""
    if current_user.get('role') != 'admin':
        return jsonify({"error": "Unauthorized: Only admins can delete equipment"}), 403

    success = Equipment.delete(equipment_id)
    
    if success:
        return jsonify({"message": f"Equipment with ID {equipment_id} deleted successfully."}), 200
    else:
        return jsonify({"error": "Equipment not found or deletion failed"}), 404
