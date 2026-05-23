from flask import Blueprint, request, jsonify
from app.database.pool import get_conn, put_conn
from app.models import gradient as gradient_model
from app.models import favorite as favorite_model
from app.services import ServiceError
from app.middleware.auth import require_auth

favorites_bp = Blueprint('favorites', __name__, url_prefix='/api/favorites')


@favorites_bp.route('', methods=['GET'])
@require_auth
def get_favorites():
    conn = None
    try:
        conn = get_conn()
        gradients = favorite_model.list_by_user(conn, request.user_id)
        return jsonify({
            'data': gradients,
            'total': len(gradients)
        })
    except Exception as e:
        print(f"获取收藏错误: {e}")
        return jsonify({'error': '获取收藏失败'}), 500
    finally:
        if conn:
            put_conn(conn)


@favorites_bp.route('/<int:gradient_id>', methods=['POST'])
@require_auth
def add_favorite(gradient_id):
    conn = None
    try:
        conn = get_conn()
        
        gradient = gradient_model.find_by_id(conn, gradient_id)
        if not gradient:
            return jsonify({'error': '方案不存在'}), 404
        
        if not gradient['is_public']:
            return jsonify({'error': '只能收藏公开方案'}), 400
        
        if gradient['user_id'] == request.user_id:
            return jsonify({'error': '不能收藏自己的方案'}), 400
        
        if favorite_model.exists(conn, request.user_id, gradient_id):
            return jsonify({'error': '已经收藏过此方案'}), 409
        
        favorite_model.add(conn, request.user_id, gradient_id)
        conn.commit()
        
        return jsonify({'message': '收藏成功'}), 201
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"收藏错误: {e}")
        return jsonify({'error': '收藏失败'}), 500
    
    finally:
        if conn:
            put_conn(conn)


@favorites_bp.route('/<int:gradient_id>', methods=['DELETE'])
@require_auth
def remove_favorite(gradient_id):
    conn = None
    try:
        conn = get_conn()
        
        favorite_model.remove(conn, request.user_id, gradient_id)
        conn.commit()
        
        return jsonify({'message': '已取消收藏'})
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"取消收藏错误: {e}")
        return jsonify({'error': '取消收藏失败'}), 500
    
    finally:
        if conn:
            put_conn(conn)
