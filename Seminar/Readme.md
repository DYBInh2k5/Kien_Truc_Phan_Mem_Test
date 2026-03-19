
# Topics

- Books: https://drive.google.com/drive/folders/1-K5Tf2YWbrms2kuPxbvRL4onJItFGBwn
- Submit:  PPTx, Code (zip file), Guide / Manual (install, libraries, command), Dockerfile (packages the service together with all required dependencies so that the service can run independently inside a container)
- Deadline: week 8

## Technical Requirements

### Microservices

* Services must be independently deployable
* Each service should have its own data (or mock database)

### gRPC

* Define at least one `.proto` file
* Implement:

  * At least one **Unary RPC**
  * At least one **Streaming RPC** (any type)

### Docker

* Each service must have its own **Dockerfile**
* Use **docker-compose** to run the entire system
* Services must communicate through Docker network

---

### Optional (Bonus)

* API Gateway
* Logging & Monitoring
* Authentication
* Message Queue integration

---

---

## C#
- CS01. Messaging (C1. Introducing Microservices , C4. First Microservice, C5. Microservice Messaging)
- CS02. Decentralizing Data (C1. Introducing Microservices , C4. First Microservice, C6. Decentralizing Data)
- CS03. Containerization (C1. Introducing Microservices , C4. First Microservice, C9. Containerization)

## Java 
- J01. API Design and Modeling (C1. Fundamentals of RESTful APIs, C2. Micronaut, C4. API Design and Modeling)
- J02. API Portfolio and Framework (C1. Fundamentals of RESTful APIs, C2. Micronaut, C5. API Portfolio and Framework)
- J03. API Platform and Data Handler (C1. Fundamentals of RESTful APIs, C2. Micronaut, C6. API Platform and Data Handler)

## GOlang
- GO01. Serialization (Chapter 1: Introduction to Microservices , Chapter 2: Scaffolding a Go Microservice, Chapter 4: Serialization)
- GO02. Synchronous (Chapter 1: Introduction to Microservices, Chapter 2: Scaffolding a Go Microservice, Chapter 5: Synchronous Communication)
- GO03. Asynchronous (Chapter 1: Introduction to Microservices, Chapter 2: Scaffolding a Go Microservice, Chapter 6: Asynchronous Communication)
  
## Python
- Py01. Python FastAPI Microservices - https://www.geeksforgeeks.org/python/microservice-in-python-using-fastapi/

🎯 Thông tin chung
Chủ đề của bạn: Py01. Python FastAPI Microservices (Xây dựng hệ thống Microservices bằng thư viện FastAPI của Python).
Hạn nộp: Tuần 8.
Sản phẩm cần nộp: Slide thuyết trình (PPTx), Source code (file cấu trúc Zip), Hướng dẫn sử dụng chi tiết (Manual), và các file cấu hình Docker.
🛠️ Yêu cầu kỹ thuật bắt buộc phải có trong code:
Giảng viên kiểm tra 3 tiêu chí cốt lõi:

Kiến trúc Microservices:

Hệ thống phải chia nhỏ thành các Service riêng biệt (ví dụ: User Service, Order Service).
Mỗi Service phải chạy độc lập và có tập dữ liệu (Database) hoặc mock-data riêng của nó.
Áp dụng giao tiếp gRPC:

Bắt buộc phải tự định nghĩa tệp 

.proto
 (Protocol Buffers).
Code phải có ít nhất 1 lệnh Unary RPC (Gọi 1-1, ví dụ: Service A gọi Service B xin thông tin 1 User).
Code phải có ít nhất 1 lệnh Streaming RPC (Giao tiếp theo luồng liên tục, ví dụ: Service A mở kết nối đẩy liên tục 100 User sang cho Service B).
Công nghệ ảo hóa Docker:

Mỗi Service phải viết một file 

Dockerfile
 riêng rẽ để đóng gói chương trình độc lập.
Bắt buộc phải viết một file 

docker-compose.yml
 định nghĩa mạng nội bộ (Docker network) để gộp toàn bộ hệ thống chạy chung một lúc và giao tiếp với nhau qua đường mạng đó.


- Py02. Python PyMS Microservices - https://python-microservices.github.io/home/
- Py03. Python ... - https://medium.com/@bittusinghtech/building-a-simple-microservices-architecture-with-python-a-step-by-step-guide-c41da2cd4631

## Nodejs
- No01. NestJS microservices (brokers, gRPC, Load balancing, Fault tolerance, ...)
- No02. Fastify (gRPC, Service discovery, Load balancing, Fault tolerance)
- No03. Moleculer (gRPC, Service discovery, Load balancing, Fault tolerance)
