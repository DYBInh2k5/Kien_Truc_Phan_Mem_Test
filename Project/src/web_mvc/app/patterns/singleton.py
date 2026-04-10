# app/patterns/singleton.py
import threading
import logging

class DatabaseConnection:
    """
    SINGLETON PATTERN (THREAD-SAFE)
    Đảm bảo chỉ có duy nhất một kết nối Database được tạo ra,
    dù cho nhiều request FastAPI gửi đến cùng một lúc (Multi-threading).
    Đây là phiên bản cực kỳ tối ưu, chống Race Condition.
    """
    _instance = None
    _lock = threading.Lock()  # Khóa Lock bảo vệ tiến trình đa luồng

    def __new__(cls):
        # Double-Checked Locking (Kiểm tra kép tối ưu hiệu năng)
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    logging.info("Tạo kết nối DB lần đầu tiên (Khởi tạo duy nhất)...")
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    
                    # Giả lập kết nối
                    cls._instance.connection_string = "Server=MainServer;DB=OrderDB;User=root;"
                    cls._instance.is_connected = True
        else:
            logging.debug("Trả về instance DB có sẵn, không tạo mới!")
            
        return cls._instance

    def query(self, sql: str) -> list[dict]:
        """Phương thức truy vấn dùng chung"""
        if self.is_connected:
            logging.info(f"DB executing: {sql}")
            return [{"status": "success", "rows": "Dummy Result"}]
        return []
