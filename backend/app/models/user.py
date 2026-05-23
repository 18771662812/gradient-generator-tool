from psycopg2.extras import RealDictCursor


def find_by_username(conn, username):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id, username, password, created_at FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    return user


def find_by_id(conn, user_id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id, username, created_at FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return {
            'id': user['id'],
            'username': user['username'],
            'created_at': user['created_at'].isoformat()
        }
    return None


def create_user(conn, username, hashed_password):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        'INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id, username, created_at',
        (username, hashed_password)
    )
    user = cursor.fetchone()
    cursor.close()
    return user
