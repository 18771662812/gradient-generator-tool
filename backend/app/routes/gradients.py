from flask import Blueprint, request, jsonify
from app.services import gradient_service
from app.services import ServiceError
from app.middleware.auth import require_auth, get_optional_auth

gradients_bp = Blueprint('gradients', __name__, url_prefix='/api/gradients')


@gradients_bp.route('/my', methods=['GET'])
@require_auth
def get_my_gradients():
    try:
        result = gradient_service.get_my_gradients(request.user_id)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gradients_bp.route('', methods=['POST'])
@require_auth
def create_gradient():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        result = gradient_service.create_gradient(request.user_id, data)
        return jsonify(result), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gradients_bp.route('/<int:gradient_id>', methods=['PUT'])
@require_auth
def update_gradient(gradient_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        result = gradient_service.update_gradient(gradient_id, request.user_id, data)
        return jsonify(result)
    
    except ServiceError as e:
        return jsonify({'error': e.message}), e.status_code
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gradients_bp.route('/<int:gradient_id>', methods=['DELETE'])
@require_auth
def delete_gradient(gradient_id):
    try:
        gradient_service.delete_gradient(gradient_id, request.user_id)
        return jsonify({'message': '删除成功'})
    
    except ServiceError as e:
        return jsonify({'error': e.message}), e.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gradients_bp.route('/<int:gradient_id>', methods=['GET'])
def get_gradient(gradient_id):
    try:
        user_id = get_optional_auth()
        result = gradient_service.get_gradient(gradient_id, user_id)
        return jsonify(result)

    except ServiceError as e:
        return jsonify({'error': e.message}), e.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gradients_bp.route('/recommend', methods=['POST'])
def recommend():
    """
    POST /api/gradients/recommend
    无需登录。
    请求体：{ "color": "#ff6b6b" }
    响应：{ "schemes": [ {name, stops, css_value, angle}, ... ] }
    """
    data = request.get_json()
    if not data or 'color' not in data:
        return jsonify({'error': '请传入 color 字段'}), 400
    try:
        result = gradient_service.recommend_gradients(data['color'])
        return jsonify(result), 200
    except ServiceError as e:
        return jsonify({'error': e.message}), e.status_code
