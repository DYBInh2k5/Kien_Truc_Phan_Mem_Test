FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY service2_order/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY service2_order/ .

# Copy proto
COPY proto/ ./proto/

# Tạo file pb2 từ Proto
RUN python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/service.proto

# Expose port (8002 cho Order)
EXPOSE 8002

# Server Order Service
CMD ["python", "main.py"]
