import os
import logging
import grpc
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import service_pb2
import service_pb2_grpc

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("OrderService")

# --- 1. MOCK DATABASE ---
ORDERS = {
    101: {"item": "Laptop Gaming", "user_id": 1, "price": 1500},
    102: {"item": "Mechanical Keyboard", "user_id": 2, "price": 120},
    103: {"item": "Wireless Mouse", "user_id": 99, "price": 50} # user 99 doesn't exist
}

# Thông số kết nối gRPC
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "localhost:50051")
GRPC_TIMEOUT = int(os.getenv("GRPC_TIMEOUT", "5")) # Timeout 5s để tránh nghẽn

app = FastAPI(
    title="Order Microservice API",
    description="Dịch vụ Đơn hàng, giao tiếp với User Service qua gRPC.",
    version="1.1"
)

# --- MODELS ---
class OrderResponse(BaseModel):
    order_id: int
    item: str
    price: float
    user_info: dict | str

# --- 2. FASTAPI REST SERVER Gọi gRPC Client ---

@app.get("/api/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    order = ORDERS.get(order_id)
    if not order:
        logger.warning(f"Order {order_id} not found.")
        raise HTTPException(status_code=404, detail="Order not found")
        
    user_data = "Unknown User"
    
    # [1] Gọi UNARY RPC sang service 1 để lấy user một cách an toàn (có timeout)
    logger.info(f"Calling User Service via gRPC for user_id={order['user_id']}")
    try:
        async with grpc.aio.insecure_channel(USER_SERVICE_URL) as channel:
            stub = service_pb2_grpc.UserServiceStub(channel)
            request = service_pb2.UserRequest(user_id=order["user_id"])
            
            # Kích hoạt timeout chống treo microservice
            response = await stub.GetUser(request, timeout=GRPC_TIMEOUT)
            
            user_data = {
                "name": response.name,
                "email": response.email
            }
            logger.info("Successfully fetched user data from User Service.")
            
    except grpc.aio.AioRpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            logger.warning("User not found in User Service.")
            user_data = "User not found"
        elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            logger.error("gRPC Timeout - User Service slow response.")
            user_data = "Service timeout"
        else:
            logger.error(f"gRPC Communication Error: {e.details()}")
            user_data = f"Service communication error: {e.details()}"

    return OrderResponse(
        order_id=order_id, 
        item=order["item"], 
        price=order["price"], 
        user_info=user_data
    )

@app.get("/api/orders/users/stream")
async def stream_all_active_users():
    """
    [2] Gọi STREAMING RPC từ service 1 để nhận dữ liệu qua luồng liên tục.
    Tối ưu hóa tài nguyên mạng khi truy xuất danh sách lớn.
    """
    async def generate_users():
        try:
            async with grpc.aio.insecure_channel(USER_SERVICE_URL) as channel:
                stub = service_pb2_grpc.UserServiceStub(channel)
                logger.info("Starting gRPC Server Streaming...")
                
                async for response in stub.StreamUsers(service_pb2.UserListRequest()):
                    yield f"Received Signal -> User ID: {response.user_id}, Name: {response.name}\n"
                    
        except grpc.aio.AioRpcError as e:
             logger.error(f"Stream broken: {e.details()}")
             yield f"Error fetching streaming data: {e.details()}\n"
             
    return StreamingResponse(generate_users(), media_type="text/plain")

@app.get("/health")
def health_check():
    """Endpoint tối ưu cho Docker Compose/Kubernetes kiểm tra sức khỏe Service"""
    return {"status": "healthy", "service": "order_service"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
