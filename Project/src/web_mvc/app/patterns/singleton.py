# app/patterns/singleton.py
import sqlite3
import threading
import logging

class DatabaseConnection:
    """
    SINGLETON PATTERN (Creational Design Pattern - Nhóm Khởi tạo)
    
    1. Mục đích:
       - Đảm bảo một Class chỉ có DUY NHẤT một thực thể (Instance) được tạo ra.
       - Cung cấp một điểm truy cập toàn cục duy nhất đến kết nối cơ sở dữ liệu SQLite (orders.db).
       
    2. Lý do áp dụng cho SQLite:
       - SQLite là hệ quản trị cơ sở dữ liệu file cục bộ, nếu có quá nhiều kết nối mở/ghi đồng thời
         từ các luồng HTTP Request khác nhau sẽ dễ gây ra lỗi "Database is locked".
       - Bằng việc áp dụng Singleton, ta chỉ dùng một đối tượng quản lý kết nối chung, giúp tiết kiệm tài nguyên.
       
    3. Cơ chế Thread-safe (An toàn đa luồng):
       - Sử dụng `threading.Lock()` làm chốt chặn khi khởi tạo.
       - Áp dụng kỹ thuật kiểm tra kép **Double-Checked Locking**:
         + Lần 1: Kiểm tra ngoài khối Lock để xem đã có instance chưa. Nếu có rồi thì bỏ qua rất nhanh (không nghẽn hiệu năng).
         + Lần 2: Nằm trong khối Lock. Nếu luồng đầu tiên đang giữ khóa lock khởi tạo xong, luồng thứ 2 sau khi chờ khóa xong
           vào đến lần kiểm tra này sẽ thấy instance đã được tạo và không khởi tạo đè lên nữa.
    """
    _instance = None
    _lock = threading.Lock() # Khóa đồng bộ đa luồng cho khởi tạo instance
    _db_file = "orders.db"   # Đường dẫn tệp tin cơ sở dữ liệu SQLite vật lý

    def __new__(cls):
        # Bước kiểm tra 1 (Double-Checked Locking): Tối ưu hóa hiệu năng, tránh nghẽn luồng khi không cần thiết
        if cls._instance is None:
            # Chỉ chiếm khóa khi chưa có instance nào được tạo
            with cls._lock:
                # Bước kiểm tra 2: Đảm bảo chắc chắn duy nhất luồng vào trước được tạo đối tượng kết nối
                if cls._instance is None:
                    logging.info("Khởi tạo instance DatabaseConnection (Singleton) lần đầu...")
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        """
        Khởi tạo cấu trúc các bảng và dữ liệu mẫu nếu chưa tồn tại trong SQLite.
        Sử dụng kết nối tạm thời để thiết lập dữ liệu ban đầu.
        """
        # check_same_thread=False cho phép kết nối được gọi từ bất kỳ luồng request nào của FastAPI
        conn = sqlite3.connect(self._db_file, check_same_thread=False)
        cursor = conn.cursor()
        
        # 1. Tạo bảng users quản lý thành viên (Xác thực chéo giữa FastAPI và C# SSO)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0
            )
        """)
        
        # 2. Tạo bảng orders quản lý thông tin đơn hàng
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                details TEXT NOT NULL,
                status TEXT NOT NULL,
                tracking_code TEXT NOT NULL
            )
        """)
        
        # Chèn dữ liệu mẫu cho users nếu database trống
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES ('admin', '123', 'admin@example.com', 1)")
            cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES ('user', '123', 'user@example.com', 0)")
            cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES ('john_doe', '123', 'john@example.com', 0)")
            cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES ('alice_smith', '123', 'alice@example.com', 0)")
            cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES ('bob_johnson', '123', 'bob@example.com', 0)")
            cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES ('moderator', '123', 'moderator@example.com', 1)")
            
        # Chèn dữ liệu mẫu cho orders nếu database trống
        cursor.execute("SELECT COUNT(*) FROM orders")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO orders (id, details, status, tracking_code) VALUES (101, 'MacBook Pro M3 (Product ID: 1) (Express) - Address: 123 Nguyen Hue, Q1', 'Shipped', 'TRACK_999')")
            cursor.execute("INSERT INTO orders (id, details, status, tracking_code) VALUES (102, 'iPhone 15 Pro Max (Product ID: 2) (Standard) - Address: 456 Le Loi, Q1', 'Pending', 'TRACK_333')")
            cursor.execute("INSERT INTO orders (id, details, status, tracking_code) VALUES (103, 'Bàn phím Leopold FC900 (Product ID: 3) (Standard) - Address: 789 CMT8, Q3', 'Paid', 'TRACK_222')")
            cursor.execute("INSERT INTO orders (id, details, status, tracking_code) VALUES (104, 'MacBook Pro M3 (Product ID: 1) (Standard) - Address: 12 Vo Van Kiet, Q5', 'Shipped', 'TRACK_555')")
            cursor.execute("INSERT INTO orders (id, details, status, tracking_code) VALUES (105, 'iPhone 15 Pro Max (Product ID: 2) (Express) - Address: 99 Nguyen Trai, Q5', 'Pending', 'TRACK_444')")
            
        conn.commit()
        conn.close()
        logging.info("Khởi tạo Database SQLite thành công với dữ liệu mẫu.")

    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        """
        Thực thi câu lệnh truy vấn SELECT.
        - Trả về: danh sách các dòng kết quả, mỗi dòng dạng dict (cột -> giá trị).
        - Đảm bảo đóng kết nối ngay sau khi hoàn thành truy vấn để giải phóng tài nguyên.
        """
        conn = sqlite3.connect(self._db_file, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Cho phép lấy cột bằng tên (ví dụ: row["username"]) thay vì chỉ số (row[0])
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
        """
        Thực thi các câu lệnh thay đổi dữ liệu (INSERT, UPDATE, DELETE).
        - Trả về: ID của dòng vừa được chèn vào (lastrowid) hoặc -1 nếu lỗi.
        - Tự động Commit nếu thành công hoặc Rollback giao dịch nếu xảy ra ngoại lệ.
        """
        conn = sqlite3.connect(self._db_file, check_same_thread=False)
        cursor = conn.cursor()
        last_id = -1
        try:
            cursor.execute(sql, params)
            conn.commit()
            last_id = cursor.lastrowid
        except Exception as e:
            logging.error(f"Lỗi thực thi SQL: {e}")
            conn.rollback() # Hoàn tác giao dịch nếu có lỗi
        finally:
            conn.close()
        return last_id
