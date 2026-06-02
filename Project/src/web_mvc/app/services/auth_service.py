# app/services/auth_service.py
from app.models.user import UserLogin, UserCreate, User
from app.patterns.singleton import DatabaseConnection

class AuthService:
    """
    BUSINESS LOGIC LAYER: Xác thực người dùng và Quản lý Users (CRUD) thông qua SQLite DB.
    """

    # --- FUNCTION: Login ---
    @staticmethod
    def login(credentials: UserLogin) -> dict:
        import urllib.request
        import json
        import logging

        # 1. Thử gọi C# SSO Microservice (Cổng 5001)
        # Sử dụng host.docker.internal để gọi từ bên trong Docker Container ra máy Windows host
        sso_url = "http://host.docker.internal:5001/api/sso/login"
        req_data = json.dumps({"username": credentials.username, "password": credentials.password}).encode("utf-8")
        req = urllib.request.Request(
            sso_url, 
            data=req_data, 
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            # Thiết lập timeout 2.0s để không gây trễ giao diện nếu service C# chưa bật
            with urllib.request.urlopen(req, timeout=2.0) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                return {
                    "message": "Đăng nhập thành công qua C# SSO!", 
                    "token": res_json.get("token"),
                    "user": {
                        "id": 999, # ID đại diện SSO
                        "username": res_json.get("user", {}).get("username", credentials.username),
                        "email": res_json.get("user", {}).get("email", "admin@sso.csharp"),
                        "is_admin": True
                    },
                    "source": "C# SSO Microservice (:5001)"
                }
        except Exception as e:
            logging.warning(f"Không kết nối được C# SSO Service ({e}). Tự động Fallback sang SQLite cục bộ...")

        # 2. Cơ chế DỰ PHÒNG (Fallback): Sử dụng database SQLite cục bộ như trước
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

    # --- FUNCTION: Managing Users ---
    @staticmethod
    def get_all_users() -> list[User]:
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

    @staticmethod
    def register_user(new_user: UserCreate) -> dict:
        db = DatabaseConnection()
        # Kiểm tra trùng username
        existing = db.query("SELECT * FROM users WHERE username = ?", (new_user.username,))
        if existing:
            return {"error": "Tên tài khoản đã tồn tại!"}
            
        new_id = db.execute(
            "INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)",
            (new_user.username, new_user.password, new_user.email, 0)
        )
        if new_id != -1:
            return {"message": f"Đăng ký thành công User ID {new_id}!"}
        return {"error": "Lỗi hệ thống khi đăng ký."}
