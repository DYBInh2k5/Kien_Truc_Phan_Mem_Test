import asyncio
import logging
import grpc
from fastapi import FastAPI
import uvicorn

# Import các file sinh ra tự động từ proto compiler (service.proto)
# - service_pb2: Chứa định nghĩa các cấu trúc Message dữ liệu (UserRequest, UserResponse,...)
# - service_pb2_grpc: Chứa các lớp Client Stub và Server Servicer
import service_pb2
import service_pb2_grpc

# --- 1. CƠ SỞ DỮ LIỆU GIẢ LẬP (MOCK DATABASE) ---
# Dữ liệu được lưu trực tiếp trên RAM dạng Dictionary để phục vụ việc demo nhanh
USERS = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Charlie", "email": "charlie@example.com"}
}

# --- 2. XỬ LÝ NGHIỆP VỤ gRPC (gRPC SERVICER) ---
# Lớp này kế thừa từ class tự động sinh ra trong file grpc để nhận các yêu cầu RPC từ bên ngoài
class UserServiceServicer(service_pb2_grpc.UserServiceServicer):
    
    # [A] Unary RPC: Nhận 1 Request từ Client, trả về đúng 1 Response ngay lập tức
    async def GetUser(self, request, context):
        logger = logging.getLogger("gRPC_GetUser")
        logger.info(f"Yêu cầu lấy thông tin User ID: {request.user_id}")
        
        user = USERS.get(request.user_id)
        if user:
            # Thành công: Trả về Message Object đúng định nghĩa của Protobuf
            return service_pb2.UserResponse(
                user_id=request.user_id, 
                name=user["name"], 
                email=user["email"]
            )
        else:
            # Thất bại: Gắn mã lỗi gRPC NOT_FOUND (tương đương lỗi HTTP 404)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return service_pb2.UserResponse()

    # [B] Server Streaming RPC: Client gửi 1 Request, Server liên tục trả về luồng dữ liệu (Stream)
    async def StreamUsers(self, request, context):
        logger = logging.getLogger("gRPC_StreamUsers")
        logger.info("Yêu cầu xuất luồng dữ liệu danh sách Users (Streaming)...")
        
        # Duyệt qua từng bản ghi trong DB giả lập
        for uid, user in USERS.items():
            # Sử dụng lệnh `yield` để đẩy dữ liệu từng bản ghi về Client ngay lập tức thay vì chờ nén lại 1 cục
            yield service_pb2.UserListResponse(user_id=uid, name=user["name"])
            # Giả lập delay độ trễ mạng 0.5s cho mỗi lần đẩy tin nhắn để demo thấy rõ luồng chảy
            await asyncio.sleep(0.5)

# --- 3. FastAPI REST SERVER (Dành cho việc truy vấn REST thông thường) ---
app = FastAPI(title="User Microservice API")

# API GET trả về JSON thô để chứng minh User Service có REST API hoạt động độc lập
@app.get("/api/users/{user_id}")
async def get_user_rest(user_id: int):
    user = USERS.get(user_id)
    if not user:
        return {"error": "User not found"}
    return user

# --- 4. KHỞI CHẠY ĐỒNG THỜI CẢ 2 SERVER TRÊN CÙNG MỘT CONTAINER ---

# Khởi chạy gRPC Server (cổng 50051)
async def serve_grpc():
    server = grpc.aio.server() # Tạo server gRPC bất đồng bộ
    # Đăng ký Service Servicer của chúng ta vào server gRPC
    service_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port('[::]:50051') # Lắng nghe trên cổng 50051 nội bộ
    await server.start()
    logging.info("gRPC Server started on port 50051")
    await server.wait_for_termination() # Giữ kết nối mở liên tục

# Khởi chạy FastAPI Web Server (cổng 8001)
async def serve_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=8001)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Sử dụng asyncio.gather để chạy song song cả 2 tác vụ không chặn (non-blocking) lẫn nhau
    await asyncio.gather(serve_grpc(), serve_fastapi())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    asyncio.run(main())
