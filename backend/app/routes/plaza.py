from flask import Blueprint, jsonify
from app.services import gradient_service
from app.middleware.auth import get_optional_auth

plaza_bp = Blueprint('plaza', __name__, url_prefix='/api/plaza')


@plaza_bp.route('', methods=['GET'])
def get_plaza():
    try:
        user_id = get_optional_auth()
        result = gradient_service.get_plaza(user_id)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
