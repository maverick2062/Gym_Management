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
    # Security Check: Only admins and employees can view the full member list
    if current_user['role'] not in ['admin', 'IT', 'Trainer']:
        return jsonify({"error": "Unauthorized access"}), 403

    members = Member.get_all()
    
    # Convert the list of Member objects into a list of dictionaries
    members_list = [
        {
            "member_id": m.member_ID, 
            "name": m.name, 
            "email": m.email, 
            "status": m.status,
            "phone_number": m.phone_number,
            "membership_plan": m.membership_plan,
            "join_date": m.join_date.strftime('%Y-%m-%d') if m.join_date else None
        } 
        for m in members
    ]
    
    return jsonify(members_list), 200

@member_bp.route('/<int:member_id>', methods=['GET'])
@token_required
def get_member_by_id(current_user, member_ID):
    """API endpoint to get a single member by their ID."""
    member = Member.find_by_id(member_ID)
    if member:
        return jsonify({
            "member_id": member.member_ID, 
            "name": member.name, 
            "email": member.email,
            "status": member.status,
            "phone_number": member.phone_number,
            "membership_plan": member.membership_plan,
            "join_date": member.join_date.strftime('%Y-%m-%d') if member.join_date else None
        }), 200
    else:
        return jsonify({"error": "Member not found"}), 404

@member_bp.route('/<int:member_ID>', methods=['PUT'])
@token_required
def update_member(current_user, member_ID):
    """API endpoint to update an existing member's details."""
    if current_user['role'] not in ['admin', 'IT']:
         return jsonify({"error": "Unauthorized: Only admins or IT can update member details"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    updated_member = Member.update(member_ID, data)
    
    if updated_member:
        return jsonify({"message": "Member updated successfully"}), 200
    else:
        return jsonify({"error": "Member not found or update failed"}), 404

@member_bp.route('/<int:member_id>', methods=['DELETE'])
@token_required
def delete_member(current_user, member_ID):
    """API endpoint to delete a member."""
    if current_user['role'] != 'admin':
        return jsonify({"error": "Unauthorized: Only admins can delete members"}), 403

    success = Member.delete(member_ID)
    
    if success:
        return jsonify({"message": f"Member with ID {member_ID} deleted successfully."}), 200
    else:
        return jsonify({"error": "Member not found or deletion failed"}), 404
