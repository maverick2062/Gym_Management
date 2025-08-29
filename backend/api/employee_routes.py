from flask import Blueprint, request, jsonify
from .auth_routes import token_required
from .employee import Employee

# Create a Blueprint for employee-related routes
employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('/', methods=['GET'])
@token_required
def get_all_employees(current_user):
    """API endpoint to get a list of all employees."""
    # Add a security check: only admins should see all employees
    if current_user.get('role') != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    employees = Employee.get_all()
    
    # Convert the list of Employee objects into a list of dictionaries
    employees_list = [
        {"user_id": emp.user_id, "name": emp.name, "email": emp.email, "role": emp.role} 
        for emp in employees
    ]
    
    return jsonify(employees_list), 200

@employee_bp.route('/<int:employee_id>', methods=['GET'])
@token_required
def get_employee_by_id(current_user, employee_id):
    """API endpoint to get a single employee by their ID."""
    if current_user.get('role') != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    employee = Employee.find_by_id(employee_id)
    if employee:
        return jsonify({
            "user_id": employee.user_id, 
            "name": employee.name, 
            "email": employee.email, 
            "role": employee.role
        }), 200
    else:
        return jsonify({"error": "Employee not found"}), 404

@employee_bp.route('/add', methods=['POST'])
@token_required
def add_employee(current_user):
    """API endpoint to add a new employee."""
    if current_user.get('role') != 'admin':
        return jsonify({"error": "Unauthorized: Only admins can add employees"}), 403

    data = request.get_json()
    required_fields = ['name', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_employee = Employee.create(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data['role'],
        salary=data.get('salary', 0)
    )

    if new_employee:
        return jsonify({
            "message": "Employee added successfully",
            "employee": {"user_id": new_employee.user_id, "name": new_employee.name}
        }), 201
    else:
        return jsonify({"error": "Failed to add employee. Email may already exist."}), 409

@employee_bp.route('/<int:employee_id>', methods=['PUT'])
@token_required
def update_employee(current_user, employee_id):
    """API endpoint to update an existing employee."""
    if current_user.get('role') != 'admin':
        return jsonify({"error": "Unauthorized: Only admins can update employee details"}), 403
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    updated_employee = Employee.update(employee_id, data)
    
    if updated_employee:
        return jsonify({"message": "Employee updated successfully"}), 200
    else:
        return jsonify({"error": "Employee not found or update failed"}), 404

@employee_bp.route('/<int:employee_id>', methods=['DELETE'])
@token_required
def delete_employee(current_user, employee_id):
    """API endpoint to delete an employee."""
    if current_user.get('role') != 'admin':
        return jsonify({"error": "Unauthorized: Only admins can delete employees"}), 403

    success = Employee.delete(employee_id)
    
    if success:
        return jsonify({"message": f"Employee with ID {employee_id} deleted successfully."}), 200
    else:
        return jsonify({"error": "Employee not found or deletion failed"}), 404
