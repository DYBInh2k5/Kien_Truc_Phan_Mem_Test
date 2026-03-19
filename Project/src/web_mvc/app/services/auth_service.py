# app/services/auth_service.py
from app.models.user import UserLogin, UserCreate, User

# Giả lập Database của SSO/User
MOCK_USERS_DB = [
    {"id": 1, "username": "admin", "password": "123", "email": "admin@example.com", "is_admin": True},
    {"id": 2, "username": "user", "password": "123", "email": "user@example.com", "is_admin": False}
]

class AuthService:
    """
    BUSINESS LOGIC LAYER: Xác thực người dùng và Quản lý Users (CRUD)
    """

    # --- FUNCTION: Login ---
    @staticmethod
    def login(credentials: UserLogin) -> dict:
        for u in MOCK_USERS_DB:
            if u["username"] == credentials.username and u["password"] == credentials.password:
                return {"message": "Đăng nhập thành công!", "token": f"fake_jwt_{u['id']}"}
        return {"error": "Tài khoản hoặc mật khẩu không chính xác."}

    # --- FUNCTION: Managing Users ---
    @staticmethod
    def get_all_users() -> list[User]:
        return [User(**u) for u in MOCK_USERS_DB]

    @staticmethod
    def register_user(new_user: UserCreate) -> dict:
        new_id = len(MOCK_USERS_DB) + 1
        user_dict = new_user.dict()
        user_dict["id"] = new_id
        user_dict["is_admin"] = False
        MOCK_USERS_DB.append(user_dict)
        return {"message": f"Đăng ký thành công User ID {new_id}!"}
