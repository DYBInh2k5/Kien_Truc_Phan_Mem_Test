# app/patterns/singleton.py
import sqlite3
import threading
import logging

class DatabaseConnection:
    """
    SINGLETON PATTERN (THREAD-SAFE)
    Đảm bảo chỉ có duy nhất một kết nối Database (hoặc đối tượng quản lý kết nối)
    được tạo ra và dùng chung cho toàn bộ ứng dụng, tránh lãng phí tài nguyên và Race Condition.
    Kết nối thực tế tới SQLite DB file.
    """
    _instance = None
    _lock = threading.Lock()
    _db_file = "orders.db"

    def __new__(cls):
        # Double-Checked Locking (Kiểm tra kép)
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    logging.info("Khởi tạo instance DatabaseConnection (Singleton) lần đầu...")
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        """Khởi tạo cấu trúc các bảng và dữ liệu mẫu nếu chưa có"""
        conn = sqlite3.connect(self._db_file, check_same_thread=False)
        cursor = conn.cursor()
        
        # 1. Tạo bảng users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0
            )
        """)
        
        # 2. Tạo bảng orders
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                details TEXT NOT NULL,
                status TEXT NOT NULL,
                tracking_code TEXT NOT NULL
            )
        """)
        
        # Chèn dữ liệu mẫu cho users nếu chưa có
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES ('admin', '123', 'admin@example.com', 1)")
            cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES ('user', '123', 'user@example.com', 0)")
            
        # Chèn dữ liệu mẫu cho orders nếu chưa có
        cursor.execute("SELECT COUNT(*) FROM orders")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO orders (id, details, status, tracking_code) VALUES (101, 'Laptop XYZ', 'Shipped', 'TRACK_999')")
            cursor.execute("INSERT INTO orders (id, details, status, tracking_code) VALUES (102, 'Bàn Phím Cơ', 'Pending', 'TRACK_333')")
            
        conn.commit()
        conn.close()
        logging.info("Khởi tạo Database SQLite thành công với dữ liệu mẫu.")

    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        """Thực thi câu lệnh SELECT và trả về danh sách dict"""
        conn = sqlite3.connect(self._db_file, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Cho phép lấy cột bằng tên
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Lỗi truy vấn SQL: {e}")
            return []
        finally:
            conn.close()

    def execute(self, sql: str, params: tuple = ()) -> int:
        """Thực thi INSERT, UPDATE, DELETE và trả về id của dòng vừa tác động (nếu có)"""
        conn = sqlite3.connect(self._db_file, check_same_thread=False)
        cursor = conn.cursor()
        last_id = -1
        try:
            cursor.execute(sql, params)
            conn.commit()
            last_id = cursor.lastrowid
        except Exception as e:
            logging.error(f"Lỗi thực thi SQL: {e}")
            conn.rollback()
        finally:
            conn.close()
        return last_id
