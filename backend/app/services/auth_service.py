from app.database.pool import get_conn, put_conn
from app.models import user as user_model
from app.services import ConflictError
from app.middleware.auth import hash_password, verify_password, generate_token


def register(username, password):
    if not username or len(username) < 3 or len(username) > 20:
        raise ValueError('用户名必须为3-20位字符')
    
    if not username.isalnum():
        raise ValueError('用户名只能包含字母和数字')
    
    if len(password) < 6:
        raise ValueError('密码至少需要6位')
    
    conn = None
    try:
        conn = get_conn()
        
        existing_user = user_model.find_by_username(conn, username)
        if existing_user:
            raise ConflictError('用户名已存在')
        
        hashed_password = hash_password(password)
        user = user_model.create_user(conn, username, hashed_password)
        conn.commit()
        
        token = generate_token(user['id'], user['username'])
        
        return {
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username']
            }
        }
    
    except (ValueError, ConflictError):
        if conn:
            conn.rollback()
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"注册错误: {e}")
        raise Exception('注册失败，请稍后重试')
    
    finally:
        if conn:
            put_conn(conn)


def login(username, password):
    conn = None
    try:
        conn = get_conn()
        
        user = user_model.find_by_username(conn, username)
        
        if not user or not verify_password(password, user['password']):
            raise ValueError('用户名或密码错误')
        
        token = generate_token(user['id'], user['username'])
        
        return {
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username']
            }
        }
    
    except ValueError:
        raise
    except Exception as e:
        print(f"登录错误: {e}")
        raise Exception('登录失败，请稍后重试')
    
    finally:
        if conn:
            put_conn(conn)


def get_user_info(user_id):
    conn = None
    try:
        conn = get_conn()
        
        user = user_model.find_by_id(conn, user_id)
        
        if not user:
            raise ValueError('用户不存在')
        
        return user
    
    except ValueError:
        raise
    except Exception as e:
        print(f"获取用户信息错误: {e}")
        raise Exception('获取用户信息失败')
    
    finally:
        if conn:
            put_conn(conn)
