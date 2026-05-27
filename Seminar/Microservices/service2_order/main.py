import os
import logging
import grpc
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Import các file sinh ra tự động từ proto compiler (service.proto)
import service_pb2
import service_pb2_grpc

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("OrderService")

# --- 1. CƠ SỞ DỮ LIỆU GIẢ LẬP (MOCK DATABASE) ---
# Dữ liệu Đơn hàng lưu trên RAM. 
# Chú ý: Order 103 chứa `user_id = 99` không tồn tại trong User Service để test lỗi gRPC NOT_FOUND
ORDERS = {
    101: {"item": "Laptop Gaming", "user_id": 1, "price": 1500},
    102: {"item": "Mechanical Keyboard", "user_id": 2, "price": 120},
    103: {"item": "Wireless Mouse", "user_id": 99, "price": 50}
}

# Cấu hình địa chỉ gRPC Server (Được Docker định tuyến qua hostname `user-service` ở cổng 50051)
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "localhost:50051")
# Cơ chế Timeout: Ngắt kết nối sau 5s nếu server gặp sự cố hoặc nghẽn mạng để chống treo app
GRPC_TIMEOUT = int(os.getenv("GRPC_TIMEOUT", "5"))

app = FastAPI(
    title="Order Microservice API",
    description="Dịch vụ Đơn hàng, giao tiếp với User Service qua gRPC.",
    version="1.1"
)

# --- 2. ĐỊNH NGHĨA PYDANTIC MODEL (DATA VALIDATION) ---
class OrderResponse(BaseModel):
    order_id: int
    item: str
    price: float
    user_info: dict | str # Chứa thông tin User trả về từ gRPC hoặc thông báo lỗi

# --- 3. FASTAPI ENDPOINT GỌI gRPC CLIENT ---

# API REST 1: Lấy chi tiết đơn hàng (Sử dụng Unary RPC)
@app.get("/api/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    order = ORDERS.get(order_id)
    if not order:
        logger.warning(f"Order {order_id} không tìm thấy trên hệ thống.")
        raise HTTPException(status_code=404, detail="Order not found")
        
    user_data = "Unknown User"
    
    logger.info(f"Đang thiết lập kết nối gRPC tới User Service tại {USER_SERVICE_URL} cho user_id={order['user_id']}")
    try:
        # [A] Tạo kênh truyền gRPC không mã hóa (insecure channel) bất đồng bộ
        async with grpc.aio.insecure_channel(USER_SERVICE_URL) as channel:
            # Khởi tạo Client Stub để triệu gọi các hàm từ xa
            stub = service_pb2_grpc.UserServiceStub(channel)
            request = service_pb2.UserRequest(user_id=order["user_id"])
            
            # Thực thi gọi hàm Unary RPC GetUser, truyền vào tham số timeout
            response = await stub.GetUser(request, timeout=GRPC_TIMEOUT)
            
            # Nhận kết quả thành công và gán vào object JSON
            user_data = {
                "name": response.name,
                "email": response.email
            }
            logger.info("Lấy thông tin User qua gRPC thành công.")
            
    except grpc.aio.AioRpcError as e:
        # Bắt các mã lỗi trả về từ gRPC Server để trả về thông báo lỗi phù hợp
        if e.code() == grpc.StatusCode.NOT_FOUND:
            logger.warning("User không tồn tại (NOT_FOUND) trên User Service.")
            user_data = "User not found"
        elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            logger.error("Kết nối gRPC bị TIMEOUT (DEADLINE_EXCEEDED) do Server User phản hồi chậm.")
            user_data = "Service timeout"
        else:
            logger.error(f"Lỗi giao tiếp gRPC khác: {e.details()}")
            user_data = f"Service communication error: {e.details()}"

    return OrderResponse(
        order_id=order_id, 
        item=order["item"], 
        price=order["price"], 
        user_info=user_data
    )

# API REST 2: Lấy luồng dữ liệu (Sử dụng Server Streaming RPC)
@app.get("/api/orders/users/stream")
async def stream_all_active_users():
    """
    Endpoint này gọi sang User Service qua gRPC Stream để nhận dữ liệu liên tục dưới dạng ống dẫn (pipeline).
    Tối ưu hóa bộ nhớ RAM, dữ liệu trả về dòng nào sẽ được đẩy ngay về Client dòng đó.
    """
    async def generate_users():
        try:
            # Thiết lập kết nối gRPC
            async with grpc.aio.insecure_channel(USER_SERVICE_URL) as channel:
                stub = service_pb2_grpc.UserServiceStub(channel)
                logger.info("Khởi động gRPC Server Streaming...")
                
                # Gọi hàm StreamUsers và sử dụng async for để đọc từng gói tin response gửi về từ stream
                async for response in stub.StreamUsers(service_pb2.UserListRequest()):
                    yield f"Received Signal -> User ID: {response.user_id}, Name: {response.name}\n"
                    
        except grpc.aio.AioRpcError as e:
             logger.error(f"Đường truyền stream bị lỗi hoặc ngắt quãng: {e.details()}")
             yield f"Error fetching streaming data: {e.details()}\n"
             
    # FastAPI bọc hàm generator bất đồng bộ vào `StreamingResponse` để truyền luồng dữ liệu thô về trình duyệt
    return StreamingResponse(generate_users(), media_type="text/plain")

@app.get("/health")
def health_check():
    # Endpoint dùng cho Docker Compose hoặc Kubernetes thăm dò tình trạng của Container (Health Check)
    return {"status": "healthy", "service": "order_service"}

if __name__ == '__main__':
    import uvicorn
    # Chạy uvicorn server ở cổng 8002
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
