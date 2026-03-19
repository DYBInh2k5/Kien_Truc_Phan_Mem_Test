# app/patterns/singleton.py

class DatabaseConnection:
    """
    SINGLETON PATTERN
    Đảm bảo chỉ có duy nhất một kết nối Database được tạo ra trong toàn bộ vòng đời ứng dụng.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            # Giả lập khởi tạo kết nối database 
            cls._instance.connection_string = "Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=myPassword;"
            cls._instance.is_connected = True
            print("Database connected successfully.")
        return cls._instance

    def query(self, sql: str):
        if self.is_connected:
            print(f"Executing Query: {sql}")
            return [{"id": 1, "data": "Sample Data"}]
        return None
