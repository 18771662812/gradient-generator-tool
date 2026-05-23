from psycopg2.extras import RealDictCursor


def add(conn, user_id, gradient_id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        'INSERT INTO favorites (user_id, gradient_id) VALUES (%s, %s)',
        (user_id, gradient_id)
    )
    cursor.close()


def remove(conn, user_id, gradient_id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        'DELETE FROM favorites WHERE user_id = %s AND gradient_id = %s',
        (user_id, gradient_id)
    )
    cursor.close()


def exists(conn, user_id, gradient_id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        'SELECT 1 FROM favorites WHERE user_id = %s AND gradient_id = %s',
        (user_id, gradient_id)
    )
    result = cursor.fetchone()
    cursor.close()
    return result is not None


def list_by_user(conn, user_id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        '''SELECT g.id, g.user_id, g.name, g.type, g.angle, g.stops, g.css_value,
                  g.is_public, g.created_at, g.updated_at, u.username as author
           FROM favorites f
           JOIN gradients g ON f.gradient_id = g.id
           JOIN users u ON g.user_id = u.id
           WHERE f.user_id = %s
           ORDER BY f.created_at DESC''',
        (user_id,)
    )
    gradients = cursor.fetchall()
    cursor.close()
    result = []
    for g in gradients:
        result.append({
            'id': g['id'],
            'user_id': g['user_id'],
            'name': g['name'],
            'type': g['type'],
            'angle': g['angle'],
            'stops': g['stops'],
            'css_value': g['css_value'],
            'is_public': g['is_public'],
            'created_at': g['created_at'].isoformat(),
            'updated_at': g['updated_at'].isoformat(),
            'author': g['author']
        })
    return result
