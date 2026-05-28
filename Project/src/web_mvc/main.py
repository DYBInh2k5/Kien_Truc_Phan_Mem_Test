# web_mvc/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.controllers.api_router import router
import os

app = FastAPI(
    title="Hệ thống Quản lý Đơn hàng - Software Architecture",
    description="Đây là khối Web API (MVC / nLayers) áp dụng 5 Design Patterns: Singleton, Factory Method, Facade, State, và Iterator.",
    version="1.0"
)

# Gắn toàn bộ Router (Controller) vào App
app.include_router(router, prefix="/api")

# Tạo thư mục static nếu chưa có để tránh lỗi mount
static_dir = os.path.join(os.path.dirname(__file__), "app", "static")
os.makedirs(static_dir, exist_ok=True)

# Mount thư mục tĩnh
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Route trả về giao diện Frontend
@app.get("/")
def read_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend index.html is missing. Please create it under app/static/index.html"}

if __name__ == "__main__":
    print("Khởi động Máy chủ API...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
