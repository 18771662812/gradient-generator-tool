import colorsys
import math

from app.database.pool import get_conn, put_conn
from app.models import gradient as gradient_model
from app.services import NotFoundError, ForbiddenError, ServiceError


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


def _hex_to_hsl(hex_color: str):
    """#rrggbb → (h°, s%, l%)"""
    hex_color = hex_color.lstrip('#')
    r, g, b = (int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s * 100, l * 100


def _hsl_to_hex(h: float, s: float, l: float) -> str:
    """(h°, s%, l%) → #rrggbb"""
    h = h % 360
    s = max(0.0, min(100.0, s)) / 100.0
    l = max(0.0, min(100.0, l)) / 100.0
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
    return '#{:02x}{:02x}{:02x}'.format(
        int(round(r * 255)),
        int(round(g * 255)),
        int(round(b * 255))
    )


def _make_stops(colors: list) -> list:
    """将颜色列表均匀分配位置，生成 stops 数组"""
    n = len(colors)
    return [
        {"color": c, "position": round(i * 100 / (n - 1)) if n > 1 else 0}
        for i, c in enumerate(colors)
    ]


def _make_css(stops: list, angle: int = 135) -> str:
    parts = ', '.join(f"{s['color']} {s['position']}%" for s in stops)
    return f"linear-gradient({angle}deg, {parts})"


def recommend_gradients(hex_color: str) -> dict:
    """
    给定一个基准色，返回 5 套渐变配色方案。
    基于 HSL 色彩空间计算，无需外部依赖。
    """
    if not hex_color or not hex_color.startswith('#') or len(hex_color) != 7:
        raise ServiceError("颜色格式不正确，请传入 #rrggbb 格式", 400)

    try:
        h, s, l = _hex_to_hsl(hex_color)
    except Exception:
        raise ServiceError("颜色解析失败", 400)

    schemes = []

    # 方案1：同色深浅（亮色→原色→暗色）
    light = _hsl_to_hex(h, s * 0.7, min(l * 1.4, 90))
    dark  = _hsl_to_hex(h, min(s * 1.1, 100), max(l * 0.55, 10))
    stops1 = _make_stops([light, hex_color, dark])
    schemes.append({
        "name": "同色深浅",
        "stops": stops1,
        "css_value": _make_css(stops1),
        "angle": 135
    })

    # 方案2：互补撞色（原色→补色，H+180°）
    comp = _hsl_to_hex((h + 180) % 360, s, l)
    stops2 = _make_stops([hex_color, comp])
    schemes.append({
        "name": "互补撞色",
        "stops": stops2,
        "css_value": _make_css(stops2),
        "angle": 90
    })

    # 方案3：邻近色调（H-30° → 原色 → H+30°）
    left30  = _hsl_to_hex((h - 30) % 360, s, l)
    right30 = _hsl_to_hex((h + 30) % 360, s, l)
    stops3 = _make_stops([left30, hex_color, right30])
    schemes.append({
        "name": "邻近色调",
        "stops": stops3,
        "css_value": _make_css(stops3),
        "angle": 90
    })

    # 方案4：三角配色（原色 → H+120° → H+240°）
    tri1 = _hsl_to_hex((h + 120) % 360, s, l)
    tri2 = _hsl_to_hex((h + 240) % 360, s, l)
    stops4 = _make_stops([hex_color, tri1, tri2])
    schemes.append({
        "name": "三角配色",
        "stops": stops4,
        "css_value": _make_css(stops4),
        "angle": 135
    })

    # 方案5：莫兰迪（大幅降饱和+微调色相+提亮）
    mor1 = _hsl_to_hex(h,              s * 0.35, min(l * 1.25, 82))
    mor2 = _hsl_to_hex((h + 20) % 360, s * 0.28, min(l * 1.15, 78))
    mor3 = _hsl_to_hex((h + 40) % 360, s * 0.22, min(l * 1.05, 75))
    stops5 = _make_stops([mor1, mor2, mor3])
    schemes.append({
        "name": "莫兰迪",
        "stops": stops5,
        "css_value": _make_css(stops5),
        "angle": 135
    })

    return {"schemes": schemes}
