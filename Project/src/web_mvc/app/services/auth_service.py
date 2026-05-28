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
                }
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
