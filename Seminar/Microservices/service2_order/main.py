import os
import grpc
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

import service_pb2
import service_pb2_grpc

# --- 1. MOCK DATABASE ---
ORDERS = {
    101: {"item": "Laptop", "user_id": 1},
    102: {"item": "Mouse", "user_id": 2},
    103: {"item": "Keyboard", "user_id": 99} # user_id 99 doesn't exist
}

# Lấy URL của User-Service qua biến môi trường để gọi từ Docker mạng nội bộ
# "user_service" chính là tên container
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "localhost:50051")

app = FastAPI(title="Order Microservice API")

# --- 2. FASTAPI REST SERVER Gọi gRPC Client ---

@app.get("/api/orders/{order_id}")
async def get_order(order_id: int):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    user_data = "Unknown User"
    
    # [1] Gọi UNARY RPC sang service 1 để lấy user
    try:
        async with grpc.aio.insecure_channel(USER_SERVICE_URL) as channel:
            stub = service_pb2_grpc.UserServiceStub(channel)
            
            # Gửi Request
            request = service_pb2.UserRequest(user_id=order["user_id"])
            
            # Nhận Response
            response = await stub.GetUser(request)
            
            user_data = {
                "name": response.name,
                "email": response.email
            }
    except grpc.aio.AioRpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            user_data = "User not found"
        else:
            user_data = f"Service communication error: {e.details()}"

    return {
        "order_id": order_id, 
        "item": order["item"], 
        "user_info": user_data
    }


@app.get("/api/orders/users/stream")
async def stream_all_active_users():
    # [2] Gọi STREAMING RPC từ service 1 để lấy danh sách user dưới dạng luồng dữ liệu liên tục
    async def generate_users():
        try:
            async with grpc.aio.insecure_channel(USER_SERVICE_URL) as channel:
                stub = service_pb2_grpc.UserServiceStub(channel)
                
                # Biến "response" lấy dữ liệu dần dần do yield từ Service 1 trả về
                async for response in stub.StreamUsers(service_pb2.UserListRequest()):
                    yield f"Received User ID: {response.user_id}, Name: {response.name}\n"
        except grpc.aio.AioRpcError as e:
             yield f"Error fetching streaming data: {e.details()}\n"
             
    # StreamingResponse của FastAPI sẽ hiển thị dữ liệu dần ngay khi nhận được từ stream
    return StreamingResponse(generate_users(), media_type="text/plain")

if __name__ == '__main__':
    import uvicorn
    # Chỉ định port 8002 cho Order Service
    uvicorn.run(app, host="0.0.0.0", port=8002)
