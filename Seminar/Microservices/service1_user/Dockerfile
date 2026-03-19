FROM python:3.10-slim

WORKDIR /app

# Khai báo requiremnts
COPY service1_user/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code từ service1_user
COPY service1_user/ .

# Copy proto 
COPY proto/ ./proto/

# Chạy lệnh generate protoc để tạo ra 2 file `service_pb2.py` và `service_pb2_grpc.py`
RUN python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/service.proto

# Khai báo cổng (8001 cho REST, 50051 cho gRPC)
EXPOSE 8001
EXPOSE 50051

# Chạy server
CMD ["python", "main.py"]
