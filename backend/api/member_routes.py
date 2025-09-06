from flask import Blueprint, request, jsonify
from .auth_routes import token_required
from .user import Member

member_bp = Blueprint('member_bp', __name__)

@member_bp.route('/', methods=['GET'])
@token_required
def get_all_members(current_user):
    """
    API endpoint to get a list of all members.
    Accessible by admin, IT, and Trainer roles.
    """
    # Any authorized employee or admin can view members
    allowed_roles = ['admin', 'IT', 'Trainer']
    if current_user.get('role') not in allowed_roles:
        return jsonify({"error": "Unauthorized access"}), 403

    members = Member.get_all()
    
    # Convert member objects to a list of dictionaries for JSON serialization
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
def get_member_by_id(current_user, member_id):
    """API endpoint to get a single member by their ID."""
    allowed_roles = ['admin', 'IT', 'Trainer']
    if current_user.get('role') not in allowed_roles:
        return jsonify({"error": "Unauthorized access"}), 403

    member = Member.find_by_id(member_id)
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

@member_bp.route('/update/<int:member_id>', methods=['PUT'])
@token_required
def update_member(current_user, member_id):
    """API endpoint to update a member. Only accessible by Admin and IT."""
    allowed_roles = ['admin', 'IT']
    if current_user.get('role') not in allowed_roles:
        return jsonify({"error": "Unauthorized: You do not have permission to update members."}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    updated_member = Member.update(member_id, data)
    
    if updated_member:
        return jsonify({"message": "Member updated successfully"}), 200
    else:
        return jsonify({"error": "Member not found or update failed"}), 404

@member_bp.route('/delete/<int:member_id>', methods=['DELETE'])
@token_required
def delete_member(current_user, member_id):
    """API endpoint to delete a member. Only accessible by Admin and IT."""
    allowed_roles = ['admin', 'IT']
    if current_user.get('role') not in allowed_roles:
        return jsonify({"error": "Unauthorized: You do not have permission to delete members."}), 403

    success = Member.delete(member_id)
    
    if success:
        return jsonify({"message": f"Member with ID {member_id} deleted successfully."}), 200
    else:
        return jsonify({"error": "Member not found or deletion failed"}), 404
