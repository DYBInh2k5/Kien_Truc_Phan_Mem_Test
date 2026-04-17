# 🧠 TỔNG QUAN KIẾN THỨC CỐT LÕI (KNOWLEDGE BASE) DÀNH CHO SEMINAR MICROSERVICES

Tài liệu này tổng hợp toàn bộ lý thuyết lõi, giải thích định nghĩa các thuật ngữ kỹ thuật một cách dễ hiểu nhất để bạn dùng làm tư liệu **Trả lời vấn đáp (Q&A)** hoặc soạn nội dung chi tiết cho Slide trên lớp.

---

## 1. KHÁI NIỆM ROOT: MICROSERVICES LÀ GÌ?
*Trong 10 năm trước, lập trình viên thường nhồi nhét mọi tính năng (Login, Đặt Hàng, Thanh Toán) vào chung 1 Source Code lớn, gọi chung chung 1 Database. Đó gọi là kiến trúc **Monolithic** (Nguyên khối).*

- **Microservices** là mô hình đập tan khối đá khổng lồ đó thành hàng chục khối lego nhỏ (Services). 
- **Đặc điểm bắt buộc của Microservices:**
  - `Độc lập triển khai (Independently Deployable)`: Service này sập, Service kia vẫn sống nhăn răng.
  - `Độc lập dữ liệu (Data Isolation)`: User Service chỉ giữ bảng User, không biết Order là gì. Nếu cần, chúng phải trao đổi dữ liệu qua mạng với nhau. Mô hình Seminar của chúng ta đã mô phỏng hoàn hảo tính chất này.

---

## 2. GIAO THỨC gRPC VÀ PROTOBUF LÀ GÌ?
*Giờ đã tách rời 2 Service, làm sao lôi data của nhau? Bạn có thể gọi REST API, nhưng nhóm của bạn "đẳng cấp hơn" vì dùng gRPC.*

- **gRPC (gRPC Remote Procedure Call)**: Phát triển bởi Google. Nó cho phép một ứng dụng máy khách (Order) gọi trực tiếp 1 phương thức trên máy chủ (User) giống như thể hai đứa nó nằm chung một file code local (Local call).
- **Protobuf (Protocol Buffers)**: Bản chất giống JSON (để cấu trúc dữ liệu gửi - nhận). Điểm ăn tiền của Protobuf là nó dịch dữ liệu chữ đó thành **mã nhị phân ảo (Binary)**. 
- **Ưu điểm vượt trội của gRPC so với REST API:**
  - Nhanh gấp 10 lần REST do dữ liệu gửi đi siêu nhẹ (Binary compress).
  - Hoạt động trên giao thức `HTTP/2` tiên tiến cho phép truyền dữ liệu liên tục 2 chiều.

---

## 3. UNARY RPC VÀ STREAMING RPC KHÁC NHAU CHỖ NÀO?
*Đây là 2 kĩ thuật Code chính được yêu cầu cho bài tập này.*

- **Unary RPC (1 đổi 1)**:  
  Bạn gửi Request hỏi "Id 101 tên là gì?", Server tra cứu và trả cái đùng cục Response "Alice!". Quy trình kết thúc. (Ngắn gọn, dứt điểm).
  
- **Streaming RPC (Truyền dưới dạng Luồng Dữ Liệu)**:  
  Giống như bạn mở Vòi Nước. Bạn gửi 1 Request, Server cắm một cái ống luồng và xả Response liên tục (Ví dụ: Trả về một vạn User). Nó xả data từng mảnh về cho Client xử lý ngay mà không cần bắt Client chờ vạn User đó loading nén chung vào một File bự. Kĩ thuật này gánh tải Memory (RAM) cực khủng cho hệ thống thực tế.

---

## 4. VÌ SAO PHẢI CÓ DOCKER & DOCKER COMPOSE?
*Kiến trúc phần mềm không chỉ là Code, mà là việc Đóng gói và Xây dựng phần cứng ảo (Infrastructure).*

- **Docker Component (Containerization)**: 
  Đóng gói toàn bộ code Python, Thư viện thư mục gRPC ảo và hệ điều hành cực mỏng vào trong một con Container (Bình ắc quy nhỏ). Chép sang máy Mac hay Linux nó vẫn chạy ngon ơ không bao giờ dính lỗi "Works on my machine" (Máy tui chạy được mà sao máy anh bó tay).
- **Docker Compose (Orchestration & Network)**:
  Đây là thứ giúp các Microservices "thấy" nhau. Nó tạo ra một Local V-LAN Network ảo, cấp phát DNS tự động. Vì thế nên code Order Service của bạn chỉ cần gõ thư gửi địa chỉ `user-service` là Docker lập tức định tuyến đường mạng nội bộ chuyển Request sang Container tương ứng!

---

## 5. TẠI SAO CHỌN PYTHON FASTAPI?
- Tốc độ xứ lý bất đồng bộ (Asynchronous) thông qua thư viện `asyncio` đứng top 3 thị trường, ngang ngửa NodeJS, cực mượt.
- Hệ thống Document (Swagger UI) tự động sinh thiết kế giao diện từ Code, giúp màn hình Demo trở nên tuyệt đẹp không mất công frontend.
- Pydantic siêu việt: Tự động format và xác thực/validate dữ liệu truyền vào API.
