# 🐳 Hướng dẫn Cài đặt Docker & Setup Dự án Seminar trên Windows

Tài liệu này hướng dẫn bạn từ A-Z cách tải Docker Desktop, cài đặt nền tảng ảo hóa cho máy Windows và cách kích hoạt dự án Microservices Python của bạn bằng lệnh Docker trong 5 bước đơn giản.

---

## BƯỚC 1: Chuẩn bị Môi trường Máy tính (WSL 2)
Docker trên Windows chạy ổn định nhất thông qua Hệ thống con Linux (WSL 2 - Windows Subsystem for Linux 2).
1. Mở ô tìm kiếm Windows (Windows Search), gõ `PowerShell`, click chuột phải vào **Windows PowerShell** và chọn **Run as administrator** (Chạy bằng quyền Admin).
2. Dán dòng lệnh sau và nhấn Enter:
   ```bash
   wsl --install
   ```
3. Khởi động lại máy tính (Restart) nếu đây là lần đầu tiên bạn kích hoạt WSL.

---

## BƯỚC 2: Tải và Cài đặt Docker Desktop
1. Truy cập trang web chính thức của Docker: [**Tải Docker Desktop for Windows (Tại đây)**](https://docs.docker.com/desktop/install/windows-install/).
2. Click vào nút màu xanh có dòng chữ **"Docker Desktop for Windows"** để tải file `.exe` về máy.
3. Mở file `.exe` vừa tải. Lúc cửa sổ cài đặt hiện lên, **HÃY ĐẢM BẢO BẠN ĐÃ TÍCH CHỌN** ô có nội dung: `"Use WSL 2 instead of Hyper-V (recommended)"`. 
4. Bấm *Ok / Next* liên tục cho đến khi cài đặt xong. Đóng cửa sổ cài đặt.

---

## BƯỚC 3: Mở phần mềm Docker và Đăng nhập
1. Nhấn phím `Windows` trên bàn phím, gõ chữ `Docker Desktop` và nhấn Enter để mở phần mềm lên.
2. Một bảng "Terms and Conditions" sẽ hiện ra, chọn biểu tượng **Accept**.
3. Bạn có thể chọn *Continue Without Signing In* (Bỏ qua bước đăng nhập) hoặc tạo tài khoản miễn phí tùy ý.
4. Chờ một lúc cho vòng lốc xoáy (Engine) bên góc dưới menu xoay xong và chuyển sang biểu tượng màu xanh lá cây (**Engine Running**). *(Lưu ý: Bạn phải luôn mở phần mềm nền này thì terminal dọn lệnh mới hiểu chữ `docker` là gì).*

---

## BƯỚC 4: Kiểm tra sự Liên kết với Terminal
Bây giờ cài xong rồi, ta kiểm tra xem Windows đã nhận diện Docker chưa:
1. Mở phần mềm VS Code của bạn lên. Bật Terminal (phím tắt `Ctrl` + `~`).
2. Gõ lệnh kiểm tra phiên bản Docker:
   ```bash
   docker --version
   ```
   *(Kết quả thành công sẽ in ra dạng: `Docker version 24.x.x, build ...`)*
3. Gõ lệnh kiểm tra công cụ Compose (Công cụ đọc file `docker-compose.yml`):
   ```bash
   docker-compose --version
   ```
   *(Nhận lại kết quả tương tự phiên bản.)*

---

## BƯỚC 5: Kết nối & Build Project Seminar 🚀
Bây giờ máy tính của bạn đã chính thức được trang bị hệ thống chạy Microservices chuyên nghiệp! Ta bắt đầu kích hoạt Project:

1. Di dời Terminal vào thẳng thư mục chứa Code Seminar của bạn:
   ```bash
   cd D:\Downloads\SA-main\SA-main\Seminar\Microservices
   ```
2. **Kích nổ hệ thống:** Gõ lệnh này để Docker bắt tay vào tự download thư viện, tạo file con Python ảo và liên kết mạng gRPC cho 2 dịch vụ Order và User:
   ```bash
   docker-compose up --build
   ```
3. Chờ cho màn hình chạy xong các tiến trình báo `Done`. Nếu bạn thấy ở những dòng mạn cuối xuất hiện:
   - `python_order_service | INFO: Uvicorn running on http://0.0.0.0:8002`
   - `python_user_service | INFO: Uvicorn running on http://0.0.0.0:8001`

**🎉 XIN CHÚC MỪNG! HỆ THỐNG ĐÃ KÍCH HOẠT THÀNH CÔNG 🎉**
Bạn hãy mở trình duyệt và gõ `http://localhost:8002/docs` để biểu diễn Seminar trơn tru trên môi trường Docker thuần túy nhé! 

---
*(Mẹo nhỏ: Sau khi thuyết trình xong, bạn chỉ việc gõ `Ctrl + C` lặp lại 2 lần vào màn hình Terminal để tự động tắt Server và tắt Container dọn dẹp RAM rác).*
