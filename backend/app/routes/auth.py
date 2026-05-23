from flask import Blueprint, request, jsonify
from app.services import auth_service
from app.services import ServiceError
from app.middleware.auth import require_auth

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': '用户名和密码不能为空'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        result = auth_service.register(username, password)
        return jsonify(result), 201
    
    except ServiceError as e:
        return jsonify({'error': e.message}), e.status_code
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': '用户名和密码不能为空'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        result = auth_service.login(username, password)
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    try:
        user = auth_service.get_user_info(request.user_id)
        return jsonify({'user': user})
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
