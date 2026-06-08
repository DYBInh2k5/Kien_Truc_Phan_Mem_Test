# app/services/auth_service.py
from app.models.user import UserLogin, UserCreate, User
from app.patterns.singleton import DatabaseConnection

class AuthService:
    """
    BUSINESS LOGIC LAYER (Tầng xử lý nghiệp vụ)
    
    Chịu trách nhiệm thực thi các quy trình nghiệp vụ liên quan đến người dùng:
    - Đăng nhập (Xác thực chéo qua SSO Microservice C# với cơ chế dự phòng SQLite).
    - Lấy danh sách thành viên (CRUD Users).
    - Đăng ký người dùng mới.
    """

    # ==========================================
    # CHỨC NĂNG: ĐĂNG NHẬP (Với cơ chế Tích hợp chéo & Fallback)
    # ==========================================
    @staticmethod
    def login(credentials: UserLogin) -> dict:
        import urllib.request
        import json
        import logging

        # 1. Bước 1: Thử gửi yêu cầu xác thực tới C# SSO Microservice (Cổng 5001)
        # Sử dụng host.docker.internal để Container Python kết nối chéo ra cổng máy host Windows
        sso_url = "http://host.docker.internal:5001/api/sso/login"
        req_data = json.dumps({"username": credentials.username, "password": credentials.password}).encode("utf-8")
        req = urllib.request.Request(
            sso_url, 
            data=req_data, 
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            # Thiết lập thời gian chờ tối đa (timeout) là 2.0s để không làm đơ UI nếu C# Service chưa bật
            with urllib.request.urlopen(req, timeout=2.0) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                # Trả về kết quả thành công và Token nhận được từ C# SSO Service
                return {
                    "message": "Đăng nhập thành công qua C# SSO!", 
                    "token": res_json.get("token"),
                    "user": {
                        "id": 999, # ID ảo đại diện cho phiên đăng nhập SSO
                        "username": res_json.get("user", {}).get("username", credentials.username),
                        "email": res_json.get("user", {}).get("email", "admin@sso.csharp"),
                        "is_admin": True
                    },
                    "source": "C# SSO Microservice (:5001)"
                }
        except Exception as e:
            # Nếu xảy ra lỗi kết nối HTTP, tiến hành ghi nhật ký cảnh báo và rơi vào luồng dự phòng cục bộ
            logging.warning(f"Không kết nối được C# SSO Service ({e}). Tự động Fallback sang SQLite cục bộ...")

        # 2. Bước 2 (Fallback): Cơ chế dự phòng khi C# SSO Offline
        # Truy vấn trực tiếp cơ sở dữ liệu SQLite cục bộ để đối chiếu thông tin đăng nhập
        db = DatabaseConnection()
        users = db.query(
            "SELECT * FROM users WHERE username = ? AND password = ?", 
            (credentials.username, credentials.password)
        )
        if users:
            user = users[0]
            is_admin_bool = bool(user["is_admin"])
            return {
                "message": "Đăng nhập thành công!", 
                "token": f"fake_jwt_{user['id']}",
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "is_admin": is_admin_bool
                },
                "source": "SQLite Local Database (Fallback)"
            }
        return {"error": "Tài khoản hoặc mật khẩu không chính xác."}

    # ==========================================
    # CHỨC NĂNG: LẤY DANH SÁCH USER
    # ==========================================
    @staticmethod
    def get_all_users() -> list[User]:
        """
        Truy vấn danh sách người dùng từ SQLite cục bộ.
        - Chuyển đổi dữ liệu thô (raw Row) sang mô hình User của Pydantic để chuẩn hóa đầu ra.
        """
        db = DatabaseConnection()
        users_raw = db.query("SELECT * FROM users")
        users = []
        for u in users_raw:
            users.append(User(
                id=u["id"],
                username=u["username"],
                email=u["email"],
                is_admin=bool(u["is_admin"])
            ))
        return users

    # ==========================================
    # CHỨC NĂNG: ĐĂNG KÝ USER MỚI
    # ==========================================
    @staticmethod
    def register_user(new_user: UserCreate) -> dict:
        """
        Đăng ký một người dùng mới vào database SQLite.
        - Bước 1: Kiểm tra xem username đã tồn tại trong database chưa để tránh xung đột dữ liệu.
        - Bước 2: Thực thi chèn dòng mới vào bảng `users`.
        """
        db = DatabaseConnection()
        # Kiểm tra trùng lặp tên tài khoản
        existing = db.query("SELECT * FROM users WHERE username = ?", (new_user.username,))
        if existing:
            return {"error": "Tên tài khoản đã tồn tại trên hệ thống!"}
            
        # Chèn người dùng mới mặc định là tài khoản thường (is_admin = 0)
        new_id = db.execute(
            "INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)",
            (new_user.username, new_user.password, new_user.email, 0)
        )
        if new_id != -1:
            return {"message": f"Đăng ký thành công User ID {new_id}!"}
        return {"error": "Lỗi hệ thống trong quá trình đăng ký."}
