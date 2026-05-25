import re
from app.database.pool import init_pool, get_conn, put_conn
from app import create_app


def init_database():
    """Execute init.sql to create tables if they don't exist."""
    conn = get_conn()
    cursor = conn.cursor()
    with open('init.sql', 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove single-line comments (-- ...)
    content = re.sub(r'--.*$', '', content, flags=re.MULTILINE)

    # Split by semicolons, skip empty blocks
    statements = [s.strip() for s in content.split(';') if s.strip()]

    for stmt in statements:
        cursor.execute(stmt)

    conn.commit()
    cursor.close()
    put_conn(conn)
    print("数据库表初始化完成")


init_pool()
init_database()
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
