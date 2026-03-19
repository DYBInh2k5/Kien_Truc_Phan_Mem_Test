import asyncio
import logging
import grpc
from fastapi import FastAPI
import uvicorn

# auto-generated grpc files
import service_pb2
import service_pb2_grpc

# --- 1. MOCK DATABASE ---
USERS = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Charlie", "email": "charlie@example.com"}
}

# --- 2. gRPC SERVICER ---
class UserServiceServicer(service_pb2_grpc.UserServiceServicer):
    
    # Unary RPC
    async def GetUser(self, request, context):
        user = USERS.get(request.user_id)
        if user:
            return service_pb2.UserResponse(
                user_id=request.user_id, 
                name=user["name"], 
                email=user["email"]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return service_pb2.UserResponse()

    # Streaming RPC (Server Streaming)
    async def StreamUsers(self, request, context):
        for uid, user in USERS.items():
            yield service_pb2.UserListResponse(user_id=uid, name=user["name"])
            await asyncio.sleep(0.5) # Giả lập delay độ trễ mạng khi stream

# --- 3. FastAPI REST SERVER ---
app = FastAPI(title="User Microservice API")

@app.get("/api/users/{user_id}")
async def get_user_rest(user_id: int):
    return USERS.get(user_id, {"error": "Not found"})

# --- 4. RUN BOTH SERVERS CONCURRENTLY ---
async def serve_grpc():
    server = grpc.aio.server()
    service_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    logging.info("gRPC Server started on port 50051")
    await server.wait_for_termination()

async def serve_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=8001)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Chạy song song cả gRPC và FastAPI server cho Service 1
    await asyncio.gather(serve_grpc(), serve_fastapi())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
