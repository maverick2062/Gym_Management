from flask import Blueprint, request, jsonify
from .auth_routes import token_required
from .user import Member

member_bp = Blueprint('member_bp', __name__)

@member_bp.route('/', methods=['GET'])
@token_required
def get_all_members(current_user):
    """
    API endpoint to get a list of all members.
    Accessible only by authenticated users.
    """
    # For extra security, you could check the role of the current_user
    # if current_user['role'] not in ['admin', 'employee']:
    #     return jsonify({"error": "Unauthorized access"}), 403

    members = Member.get_all() # This method needs to be created in the Member class
    
    # Convert the list of Member objects into a list of dictionaries
    members_list = [
        {"member_id": m.member_id, "name": m.name, "email": m.email, "password": m.password, "status": m.status} 
        for m in members
    ]
    
    return jsonify(members_list), 200

@member_bp.route('/<int:member_id>', methods=['GET'])
@token_required
def get_member_by_id(current_user, member_id):
    """API endpoint to get a single member by their ID."""
    member = Member.find_by_id(member_id) # This method needs to be created
    if member:
        return jsonify({
            "member_id": member.member_id, 
            "name": member.name, 
            "email": member.email,
            "password": member.password,
            "status": member.status
        }), 200
    else:
        return jsonify({"error": "Member not found"}), 404

@member_bp.route('/<int:member_id>', methods=['PUT'])
@token_required
def update_member(current_user, member_id):
    """API endpoint to update an existing member's details."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    updated_member = Member.update(member_id, data) # This method needs to be created
    
    if updated_member:
        return jsonify({"message": "Member updated successfully"}), 200
    else:
        return jsonify({"error": "Member not found or update failed"}), 404

@member_bp.route('/<int:member_id>', methods=['DELETE'])
@token_required
def delete_member(current_user, member_id):
    """API endpoint to delete a member."""
    # Add role check for extra security
    if current_user['role'] != 'admin':
        return jsonify({"error": "Unauthorized: Only admins can delete members"}), 403

    success = Member.delete(member_id) # This method needs to be created
    
    if success:
        return jsonify({"message": f"Member with ID {member_id} deleted successfully."}), 200
    else:
        return jsonify({"error": "Member not found or deletion failed"}), 404
