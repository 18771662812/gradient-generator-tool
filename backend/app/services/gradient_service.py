from app.database.pool import get_conn, put_conn
from app.models import gradient as gradient_model
from app.services import NotFoundError, ForbiddenError


def get_my_gradients(user_id):
    conn = None
    try:
        conn = get_conn()
        gradients = gradient_model.list_by_user(conn, user_id)
        return {
            'data': gradients,
            'total': len(gradients)
        }
    except Exception as e:
        print(f"获取我的方案错误: {e}")
        raise Exception('获取方案失败')
    finally:
        if conn:
            put_conn(conn)


def create_gradient(user_id, data):
    required_fields = ['type', 'angle', 'stops', 'css_value']
    for field in required_fields:
        if field not in data:
            raise ValueError(f'缺少必填字段: {field}')
    
    if data['type'] not in ['linear', 'radial']:
        raise ValueError('type 必须是 linear 或 radial')
    
    try:
        angle = int(data['angle'])
        if angle < 0 or angle > 360:
            raise ValueError('angle 必须在 0-360 之间')
    except (ValueError, TypeError):
        raise ValueError('angle 必须是整数')
    
    if not isinstance(data['stops'], list) or len(data['stops']) < 2:
        raise ValueError('stops 必须是至少包含2个元素的数组')
    
    name = data.get('name', '未命名方案')
    is_public = data.get('is_public', False)
    
    conn = None
    try:
        conn = get_conn()
        gradient = gradient_model.create(
            conn, user_id, name, data['type'], angle, 
            data['stops'], data['css_value'], is_public
        )
        conn.commit()
        return {
            'data': gradient,
            'message': '保存成功'
        }
    except ValueError:
        if conn:
            conn.rollback()
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"创建方案错误: {e}")
        raise Exception('创建方案失败')
    finally:
        if conn:
            put_conn(conn)


def update_gradient(gradient_id, user_id, data):
    conn = None
    try:
        conn = get_conn()
        
        gradient = gradient_model.find_by_id(conn, gradient_id)
        if not gradient:
            raise NotFoundError('方案不存在')
        
        if gradient['user_id'] != user_id:
            raise ForbiddenError('无权修改此方案')
        
        update_fields = {}
        if 'name' in data:
            update_fields['name'] = data['name']
        if 'is_public' in data:
            update_fields['is_public'] = data['is_public']
        
        if not update_fields:
            raise ValueError('没有可更新的字段')
        
        updated_gradient = gradient_model.update(conn, gradient_id, **update_fields)
        conn.commit()
        
        return {
            'data': updated_gradient,
            'message': '更新成功'
        }
    except (ValueError, NotFoundError, ForbiddenError):
        if conn:
            conn.rollback()
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"更新方案错误: {e}")
        raise Exception('更新方案失败')
    finally:
        if conn:
            put_conn(conn)


def delete_gradient(gradient_id, user_id):
    conn = None
    try:
        conn = get_conn()
        
        gradient = gradient_model.find_by_id(conn, gradient_id)
        if not gradient:
            raise NotFoundError('方案不存在')
        
        if gradient['user_id'] != user_id:
            raise ForbiddenError('无权删除此方案')
        
        gradient_model.delete(conn, gradient_id)
        conn.commit()
    except (NotFoundError, ForbiddenError):
        if conn:
            conn.rollback()
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"删除方案错误: {e}")
        raise Exception('删除方案失败')
    finally:
        if conn:
            put_conn(conn)


def get_gradient(gradient_id, current_user_id=None):
    conn = None
    try:
        conn = get_conn()
        
        gradient = gradient_model.find_by_id(conn, gradient_id)
        if not gradient:
            raise NotFoundError('方案不存在')
        
        if not gradient['is_public'] and gradient['user_id'] != current_user_id:
            raise ForbiddenError('无权访问此方案')
        
        return {'data': gradient}
    except (NotFoundError, ForbiddenError):
        raise
    except Exception as e:
        print(f"获取方案错误: {e}")
        raise Exception('获取方案失败')
    finally:
        if conn:
            put_conn(conn)


def get_plaza(current_user_id=None):
    conn = None
    try:
        conn = get_conn()
        gradients = gradient_model.list_public(conn, current_user_id)
        return {
            'data': gradients,
            'total': len(gradients)
        }
    except Exception as e:
        print(f"获取广场数据错误: {e}")
        raise Exception('获取广场数据失败')
    finally:
        if conn:
            put_conn(conn)
