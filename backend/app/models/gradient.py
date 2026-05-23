import json
from psycopg2.extras import RealDictCursor


def create(conn, user_id, name, type_, angle, stops, css_value, is_public):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        '''INSERT INTO gradients (user_id, name, type, angle, stops, css_value, is_public)
           VALUES (%s, %s, %s, %s, %s, %s, %s)
           RETURNING id, user_id, name, type, angle, stops, css_value, is_public, 
                     created_at, updated_at''',
        (user_id, name, type_, angle, json.dumps(stops), css_value, is_public)
    )
    gradient = cursor.fetchone()
    cursor.close()
    return {
        'id': gradient['id'],
        'user_id': gradient['user_id'],
        'name': gradient['name'],
        'type': gradient['type'],
        'angle': gradient['angle'],
        'stops': gradient['stops'],
        'css_value': gradient['css_value'],
        'is_public': gradient['is_public'],
        'created_at': gradient['created_at'].isoformat(),
        'updated_at': gradient['updated_at'].isoformat()
    }


def find_by_id(conn, gradient_id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        '''SELECT id, user_id, name, type, angle, stops, css_value, is_public,
                  created_at, updated_at FROM gradients WHERE id = %s''',
        (gradient_id,)
    )
    gradient = cursor.fetchone()
    cursor.close()
    if gradient:
        return {
            'id': gradient['id'],
            'user_id': gradient['user_id'],
            'name': gradient['name'],
            'type': gradient['type'],
            'angle': gradient['angle'],
            'stops': gradient['stops'],
            'css_value': gradient['css_value'],
            'is_public': gradient['is_public'],
            'created_at': gradient['created_at'].isoformat(),
            'updated_at': gradient['updated_at'].isoformat()
        }
    return None


def list_by_user(conn, user_id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        '''SELECT id, user_id, name, type, angle, stops, css_value, is_public, 
                  created_at, updated_at 
           FROM gradients WHERE user_id = %s ORDER BY created_at DESC''',
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
            'updated_at': g['updated_at'].isoformat()
        })
    return result


def list_public(conn, current_user_id=None):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    if current_user_id:
        cursor.execute(
            '''SELECT g.id, g.user_id, g.name, g.type, g.angle, g.stops, g.css_value,
                      g.is_public, g.created_at, g.updated_at, u.username as author,
                      EXISTS(SELECT 1 FROM favorites f WHERE f.user_id = %s AND f.gradient_id = g.id) as is_favorited
               FROM gradients g
               JOIN users u ON g.user_id = u.id
               WHERE g.is_public = true
               ORDER BY g.created_at DESC''',
            (current_user_id,)
        )
    else:
        cursor.execute(
            '''SELECT g.id, g.user_id, g.name, g.type, g.angle, g.stops, g.css_value,
                      g.is_public, g.created_at, g.updated_at, u.username as author,
                      false as is_favorited
               FROM gradients g
               JOIN users u ON g.user_id = u.id
               WHERE g.is_public = true
               ORDER BY g.created_at DESC'''
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
            'author': g['author'],
            'is_favorited': g['is_favorited']
        })
    return result


def update(conn, gradient_id, **fields):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    update_fields = []
    update_values = []
    
    if 'name' in fields:
        update_fields.append('name = %s')
        update_values.append(fields['name'])
    
    if 'is_public' in fields:
        update_fields.append('is_public = %s')
        update_values.append(fields['is_public'])
    
    update_fields.append('updated_at = NOW()')
    update_values.append(gradient_id)
    
    query = f'''UPDATE gradients SET {', '.join(update_fields)}
                WHERE id = %s
                RETURNING id, user_id, name, type, angle, stops, css_value, is_public,
                          created_at, updated_at'''
    
    cursor.execute(query, update_values)
    updated_gradient = cursor.fetchone()
    cursor.close()
    return {
        'id': updated_gradient['id'],
        'user_id': updated_gradient['user_id'],
        'name': updated_gradient['name'],
        'type': updated_gradient['type'],
        'angle': updated_gradient['angle'],
        'stops': updated_gradient['stops'],
        'css_value': updated_gradient['css_value'],
        'is_public': updated_gradient['is_public'],
        'created_at': updated_gradient['created_at'].isoformat(),
        'updated_at': updated_gradient['updated_at'].isoformat()
    }


def delete(conn, gradient_id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('DELETE FROM gradients WHERE id = %s', (gradient_id,))
    cursor.close()
