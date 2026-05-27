import httpx
import logging
import time
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

logging.basicConfig(level=logging.INFO, format="%(asctime)s - GATEWAY - %(levelname)s - %(message)s")
logger = logging.getLogger("Gateway")

app = FastAPI(title="API Gateway (Auth + Logging + Proxy Gateway)")

# Cấu hình chuẩn OAuth2 Password Bearer: 
# Chỉ ra rằng Client phải đăng nhập ở URL "login" và gửi kèm token dạng "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Địa chỉ Order Service nội bộ trong mạng ảo Docker (Port 8002)
ORDER_SERVICE_URL = "http://order-service:8002"

# --- 1. MIDDLEWARE: GHI NHẬT KÝ & GIÁM SÁT HỆ THỐNG (LOGGING & SURVEILLANCE) ---
# Tự động chặn mọi Request đi vào Gateway để ghi log và đo hiệu năng xử lý
@app.middleware("http")
async def intercept_logging_middleware(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Yêu cầu đi vào Gateway: {request.method} {request.url.path}")
    
    # Cho phép request đi tiếp đến router xử lý tương ứng
    response = await call_next(request)
    
    # Tính thời gian xử lý và in log kiểm soát
    process_time = time.time() - start_time
    logger.info(f"Hoàn tất xử lý sau {process_time:.3f}s với mã HTTP Status: {response.status_code}")
    return response

# --- 2. XÁC THỰC: HỆ THỐNG ĐĂNG NHẬP GIẢ LẬP (AUTHENTICATION) ---
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Hệ thống cấp quyền đăng nhập, trả về token JWT để giả lập """
    if form_data.username == "admin" and form_data.password == "123456":
        logger.info(f"Đăng nhập thành công cho tài khoản '{form_data.username}'.")
        return {"access_token": "secret_jwt_token_123", "token_type": "bearer"}
    
    logger.warning(f"Đăng nhập thất bại cho tài khoản '{form_data.username}'")
    raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không đúng")

# Dependency kiểm tra sự tồn tại và tính hợp lệ của Token trong Header
def verify_token(token: str = Depends(oauth2_scheme)):
    if token != "secret_jwt_token_123":
        logger.warning(f"Chặn đứng yêu cầu xâm nhập bất hợp pháp với Token sai lệch: {token}")
        raise HTTPException(status_code=403, detail="Yêu cầu thẻ truy cập (Token) hợp lệ/hết hạn")
    return True

# --- 3. ĐỊNH TUYẾN GATEWAY (REVERSE PROXY) ---
@app.get("/api/orders/{order_id}")
async def gateway_get_order(order_id: int, request: Request, authorized: bool = Depends(verify_token)):
    """ 
    Route Gateway chuyển tiếp (Proxy): Đã được bảo vệ bởi dependency 'verify_token'.
    Chỉ khi token hợp lệ, Gateway mới thay mặt Client gọi sâu xuống Order Service nội bộ.
    """
    logger.info("Xác thực Token thành công. Gateway bắt đầu chuyển tiếp request sang Order Service...")
    
    # Sử dụng thư viện httpx bất đồng bộ để gọi proxy ngầm sang Order Service
    async with httpx.AsyncClient() as client:
        try:
            proxy_url = f"{ORDER_SERVICE_URL}/api/orders/{order_id}"
            # Chuyển tiếp request và lấy phản hồi
            response = await client.get(proxy_url, timeout=10.0)
            
            # Trả về kết quả nguyên vẹn (dữ liệu + mã status + header) cho Client ban đầu
            return Response(
                content=response.content, 
                status_code=response.status_code, 
                media_type=response.headers.get("content-type")
            )
        except httpx.RequestError as e:
            logger.error("Không thể kết nối đến Order Service (Offline).")
            raise HTTPException(status_code=503, detail="Service 2 (Order) is temporarily down")

if __name__ == '__main__':
    import uvicorn
    # Khởi chạy Gateway Web Server ở cổng 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
