from app.database.pool import init_pool, get_conn, put_conn
from app import create_app


def init_database():
    """Execute init.sql to create tables if they don't exist."""
    try:
        conn = get_conn()
        cursor = conn.cursor()
        with open('init.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        put_conn(conn)
        print("数据库表初始化完成")
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        raise


if __name__ == '__main__':
    init_pool()
    init_database()
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
