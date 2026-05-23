import time
from psycopg2.pool import SimpleConnectionPool
from app.config import config

db_pool = None


def init_pool():
    global db_pool
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"尝试连接数据库 (第 {attempt + 1}/{max_retries} 次)...")
            db_pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=config.DB_HOST,
                port=config.DB_PORT,
                database=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD
            )
            conn = db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.close()
            db_pool.putconn(conn)
            print("数据库连接成功！")
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            if attempt < max_retries - 1:
                print(f"等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
            else:
                print("数据库连接失败，已达到最大重试次数")
                raise
    return False


def get_conn():
    if db_pool is None:
        raise Exception("数据库连接池未初始化")
    return db_pool.getconn()


def put_conn(conn):
    if db_pool is not None:
        db_pool.putconn(conn)
