import httpx
import logging
import time
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

logging.basicConfig(level=logging.INFO, format="%(asctime)s - GATEWAY - %(levelname)s - %(message)s")
logger = logging.getLogger("Gateway")

app = FastAPI(title="API Gateway (Auth + Logging + Proxy Gateway)")

# Schema Auth: Cấu hình yêu cầu bắt buộc phải có Token ở Header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ORDER_SERVICE_URL = "http://order-service:8002"

# --- 1. MIDDLEWARE: LOGGING & SURVEILLANCE ---
@app.middleware("http")
async def intercept_logging_middleware(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming Request: {request.method} {request.url.path}")
    
    # Cho phép hệ thống đi tiếp
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Completed in {process_time:.3f}s with status {response.status_code}")
    return response

# --- 2. AUTHENTICATION: LOGIN MOCK SYSTEM ---
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Hệ thống cấp quyền (Authentication). Trả về JWT Token giả để demo """
    if form_data.username == "admin" and form_data.password == "123456":
        logger.info(f"User '{form_data.username}' logged in successfully.")
        return {"access_token": "secret_jwt_token_123", "token_type": "bearer"}
    
    logger.warning(f"Failed login attempt for user '{form_data.username}'")
    raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không đúng")

# Dependency kiểm tra Token
def verify_token(token: str = Depends(oauth2_scheme)):
    if token != "secret_jwt_token_123":
        logger.warning(f"Bắt được yêu cầu xâm nhập với Token lậu: {token}")
        raise HTTPException(status_code=403, detail="Yêu cầu thẻ truy cập (Token) hợp lệ/hết hạn")
    return True

# --- 3. API GATEWAY ROUTING (Proxy) ---
@app.get("/api/orders/{order_id}")
async def gateway_get_order(order_id: int, request: Request, authorized: bool = Depends(verify_token)):
    """ 
    ROUTE GATEWAY: Đã bị khóa bởi 'verify_token'.
    Chỉ user có Token hợp lệ mới được Gateway Proxy (chuyển tiếp) sang Order Service. 
    """
    logger.info("Token Valid. Gateway is forwarding request to Order Service (gRPC trigger)...")
    
    # Gateway làm hành động chuyển tiếp HTTP sang Order Service (Đứng sau lớp mạng ảo)
    async with httpx.AsyncClient() as client:
        try:
            proxy_url = f"{ORDER_SERVICE_URL}/api/orders/{order_id}"
            response = await client.get(proxy_url, timeout=10.0)
            return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))
        except httpx.RequestError as e:
            logger.error("Order Service is offline or unreachable.")
            raise HTTPException(status_code=503, detail="Service 2 (Order) is temporarily down")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
