# Run this script to test the services locally without Docker

Write-Host "1. Creating Virtual Environment..."
python -m venv venv
.\venv\Scripts\Activate.ps1

Write-Host "2. Installing requirements..."
pip install -r service1_user\requirements.txt

Write-Host "3. Generating gRPC files..."
python -m grpc_tools.protoc -I.\proto --python_out=.\service1_user --grpc_python_out=.\service1_user .\proto\service.proto
python -m grpc_tools.protoc -I.\proto --python_out=.\service2_order --grpc_python_out=.\service2_order .\proto\service.proto

Write-Host "4. Starting Service 1 (User Service - Port 8001 & 50051) in background..."
Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "service1_user\main.py"

Write-Host "Waiting 3 seconds for Service 1 to start..."
Start-Sleep -Seconds 3

Write-Host "5. Starting Service 2 (Order Service - Port 8002). Press Ctrl+C to stop this one..."
$env:USER_SERVICE_URL="localhost:50051"
python service2_order\main.py
