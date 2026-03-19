# web_mvc/main.py
import uvicorn
from fastapi import FastAPI
from app.controllers.api_router import router

app = FastAPI(
    title="Hệ thống Quản lý Đơn hàng - Software Architecture",
    description="Đây là khối Web API (MVC / nLayers) áp dụng 5 Design Patterns: Singleton, Factory Method, Facade, State, và Iterator.",
    version="1.0"
)

# Gắn toàn bộ Router (Controller) vào App
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    print("Khởi động Máy chủ API...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
