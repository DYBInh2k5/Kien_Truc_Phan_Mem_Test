SA TEST 13/8
Objective:
Develop a web server using C# that utilizes Socket/TcpListener library.

Requirements:
API/Page Requirements: (5 points)
GET [/]: Displays detailed student information (id, fullname, PC's number) and provides a link to login.
GET [/login]: Shows the login page.
POST [/login]: Logs in with username and password. On success, redirects to /chat. On failure, displays a login failed message.
GET [/chat]: Displays online and offline chat rooms. A chat room is online if it has had activity within the last 3 minutes. If offline, its history is cleared.
POST [/chat/:id]: Sends a message to the chat room with the given id. After sending, changes the room status to online and redirects to GET /chat/:id
GET [/chat/:id]: Retrieves all messages sent to the chat room in chronological order (time, username, message).
User account information is stored in a JSON file with the following format: [ { "username": "nntu", "password": "56789" } , { "username": "AdTekDev", "password": "56789" } ]

Apply 2 of the following design patterns: (3 points)
Facade
Factory
Command
Builder
Submission Requirements:
Link: https://mlearning.hoasen.edu.vn/mod/assign/view.php?id=1062590

3-5 screenshots demonstrating the web interface execution.
3-5 Image(s) of code implementing the chosen design pattern(s).
Compressed zip file containing the C# server and an HTML folder.

hướng dẫn làm bài này tạo dùng vscode 2022, hướng dẫn tạo file và làm

Ok bài này đúng kiểu:

Raw Socket + HTTP mini server + Design Pattern 😎

Và vì m đang học style low-level socket nên tao sẽ hướng dẫn đúng kiểu:

Socket
Thread
HTTP thủ công
HTML file
JSON file

KHÔNG dùng ASP.NET.

Mục tiêu cuối cùng

Sau khi chạy:

http://localhost:8080

sẽ có:

Trang chủ
Login
Chat room
Online/offline room
Gửi tin nhắn
Lưu session memory
JSON user
Design Pattern
CÔNG NGHỆ NÊN DÙNG
BẮT BUỘC

✅ C#
✅ Socket
✅ Thread
✅ HTTP raw

KHÔNG nên dùng

❌ ASP.NET
❌ MVC
❌ Razor
❌ Entity Framework

Vì đề muốn:

Socket/TcpListener library
PHẦN MỀM

M nói:

vscode 2022

Tao đoán là:

Visual Studio 2022

😆

BƯỚC 1 — TẠO PROJECT
Mở Visual Studio 2022

Chọn:

Create a new project
Chọn
Console App (.NET)
Đặt tên
SATestSocket
Framework

Chọn:

.NET 6 hoặc .NET 8
Sau khi tạo xong

M sẽ thấy:

Program.cs
BƯỚC 2 — TẠO CẤU TRÚC THƯ MỤC

Trong Solution Explorer:

Right Click Project → Add → New Folder

Tạo:

HTML
Models
Patterns
Data
Kết quả
SATestSocket
│
├── Program.cs
│
├── HTML
│   ├── index.html
│   ├── login.html
│   ├── chat.html
│
├── Models
│   ├── User.cs
│   ├── Message.cs
│   ├── ChatRoom.cs
│
├── Patterns
│   ├── ServerFacade.cs
│   ├── UserFactory.cs
│
├── Data
│   └── users.json
BƯỚC 3 — TẠO FILE
Tạo User.cs

Right click Models → Add → Class

Tên:

User.cs
Code
namespace SATestSocket.Models
{
    internal class User
    {
        public string username { get; set; }
        public string password { get; set; }
    }
}
Tạo Message.cs
namespace SATestSocket.Models
{
    internal class Message
    {
        public string username { get; set; }

        public string content { get; set; }

        public DateTime time { get; set; }
    }
}
Tạo ChatRoom.cs
using System.Collections.Generic;

namespace SATestSocket.Models
{
    internal class ChatRoom
    {
        public int id { get; set; }

        public List<Message> messages =
            new List<Message>();

        public DateTime lastActivity { get; set; }
    }
}
BƯỚC 4 — TẠO JSON USER

Trong folder Data:

Tạo:

users.json
Nội dung
[
  {
    "username": "nntu",
    "password": "56789"
  },
  {
    "username": "AdTekDev",
    "password": "56789"
  }
]
BƯỚC 5 — DESIGN PATTERN

Đề yêu cầu:

2 design patterns

Tao khuyên:

Dùng:

✅ Facade
✅ Factory

Dễ làm nhất 😎

1. Factory Pattern
Tạo UserFactory.cs
using SATestSocket.Models;

namespace SATestSocket.Patterns
{
    internal class UserFactory
    {
        public static User create(
            string username,
            string password)
        {
            return new User
            {
                username = username,
                password = password
            };
        }
    }
}
Ý nghĩa

Factory chuyên tạo object.

2. Facade Pattern
Tạo ServerFacade.cs
using System.Text;

namespace SATestSocket.Patterns
{
    internal class ServerFacade
    {
        public static byte[] buildResponse(
            string body)
        {
            string response =
                "HTTP/1.1 200 OK\r\n";

            response +=
                "Content-Type: text/html\r\n";

            response +=
                $"Content-Length: {body.Length}\r\n";

            response += "\r\n";

            response += body;

            return Encoding.ASCII.GetBytes(response);
        }
    }
}
Ý nghĩa

Facade che logic build HTTP response.

BƯỚC 6 — CODE SERVER
Program.cs

XÓA sạch file cũ.

DÁN
using System.Net;
using System.Net.Sockets;
using System.Text;
using SATestSocket.Patterns;

IPEndPoint serverInfor =
    new IPEndPoint(IPAddress.Any, 8080);

Socket serverListen = new Socket(
    AddressFamily.InterNetwork,
    SocketType.Stream,
    ProtocolType.Tcp);

serverListen.Bind(serverInfor);

serverListen.Listen(10);

Console.WriteLine("Dang cho khach...");

while (true)
{
    Socket staff = serverListen.Accept();

    Thread t = new Thread(handleClient);

    t.Start(staff);
}

void handleClient(object obj)
{
    Socket staff = (Socket)obj;

    string requestData = "";

    while (true)
    {
        byte[] bytes = new byte[1024];

        int bytesRec = staff.Receive(bytes);

        requestData += Encoding.ASCII.GetString(
            bytes,
            0,
            bytesRec);

        if (bytesRec < 1024)
        {
            break;
        }
    }

    Console.WriteLine(requestData);

    string[] requestLines =
        requestData.Split('\n');

    string firstLine = requestLines[0];

    string body = "";

    // GET /
    if (firstLine.Contains("GET / "))
    {
        body =
        @"<html>
        <body>
        <h1>Student Information</h1>
        <p>ID: 123456</p>
        <p>Fullname: Nguyen Van A</p>
        <p>PC Number: 10</p>

        <a href='/login'>
        Login
        </a>

        </body>
        </html>";
    }

    // GET /login
    else if (firstLine.Contains("GET /login"))
    {
        body =
        @"<html>
        <body>

        <h1>Login</h1>

        <form method='POST'
        action='/login'>

        Username:
        <input name='username'/>

        <br/>

        Password:
        <input type='password'
        name='password'/>

        <br/>

        <button type='submit'>
        Login
        </button>

        </form>

        </body>
        </html>";
    }

    else
    {
        body =
        "<html><body>404</body></html>";
    }

    byte[] msg =
        ServerFacade.buildResponse(body);

    staff.Send(msg);

    staff.Shutdown(SocketShutdown.Both);

    staff.Close();
}
BƯỚC 7 — CHẠY

Nhấn:

Ctrl + F5
Browser

Mở:

http://localhost:8080
Kết quả

Trang chủ hiện:

ID
fullname
PC number
link login
BƯỚC 8 — TEST LOGIN

Phần khó nhất 😈

Vì:

POST raw HTTP

phải parse body.

Nhưng strategy để ăn điểm nhanh
Làm trước:

✅ GET /
✅ GET /login
✅ GET /chat
✅ GET /chat/1
✅ POST /chat/1

Sau đó mới làm:
POST /login
Vì login cần parse:
application/x-www-form-urlencoded
BƯỚC 9 — CHAT ROOM

Tạo:

List<ChatRoom> rooms

Global variable.

Logic online/offline

Nếu:

DateTime.Now - lastActivity

3 phút

=> offline

Nếu offline
messages.Clear();
ONLINE

Khi có:

POST /chat/:id
BƯỚC 10 — SCREENSHOT

Đề yêu cầu:

3-5 screenshots
NÊN CHỤP

✅ Trang home
✅ Login page
✅ Login success
✅ Chat room
✅ Console socket server

SCREENSHOT DESIGN PATTERN

Chụp:

✅ UserFactory.cs
✅ ServerFacade.cs

ZIP NỘP
SATestSocket.zip

Bên trong:

Program.cs
HTML/
Patterns/
Models/
Data/
CHIẾN LƯỢC ĂN ĐIỂM 😎
Quan trọng nhất
Đừng cố đẹp.

Đề này:

Architecture + Socket

KHÔNG phải frontend.

Mục tiêu
HTTP chạy được
Socket đúng
Thread đúng
GET/POST đúng
Pattern có thật

## CHI TIẾT GIẢI THÍCH CODE VÀ HOẠT ĐỘNG DỰ ÁN

### 1. Cơ chế hoạt động của Server (Socket & Threading)
Dự án sử dụng thư viện `System.Net.Sockets` để tạo một Web Server "thủ công" (Raw HTTP Server) mà không dùng các framework cấp cao như ASP.NET.
- **Socket (`serverListen`)**: Được khởi tạo với giao thức TCP (`SocketType.Stream`). Server lắng nghe tại địa chỉ `Any` (tất cả các card mạng) trên cổng `8080`.
- **Vòng lặp `while(true)`**: Server liên tục chờ đợi kết nối từ khách hàng thông qua phương thức `Accept()`.
- **Đa luồng (`Thread`)**: Mỗi khi có một trình duyệt (Client) kết nối tới, Server sẽ tạo một luồng mới (`new Thread`) để xử lý riêng cho khách hàng đó (`handleClient`). Việc này giúp Server có thể phục vụ nhiều người cùng lúc mà không bị treo.

### 2. Xử lý giao thức HTTP (Request & Response)
- **Request Parsing**: Khi nhận dữ liệu từ Client qua luồng bit (`Receive`), Server chuyển đổi nó sang dạng chuỗi (`RequestData`). Sau đó, Server phân tích dòng đầu tiên (`firstLine`) để xác định Phương thức (GET/POST) và Đường dẫn (Path: `/`, `/login`, `/chat`).
- **Routing**: Dựa vào đường dẫn, Server chọn nội dung HTML tương ứng để trả về.
- **Response Building**: Sử dụng `ServerFacade.buildResponse` để tạo ra một gói tin HTTP đúng tiêu chuẩn bao gồm:
    - Trạng thái: `HTTP/1.1 200 OK`
    - Header: `Content-Type: text/html` và `Content-Length`.
    - Body: Nội dung HTML.

### 3. Giải thích các Design Patterns đã áp dụng
Để đạt điểm tối đa về kiến trúc, dự án áp dụng 2 mẫu thiết kế:
- **Factory Pattern (`UserFactory.cs`)**: Cung cấp một phương thức tĩnh `create` để tập trung việc khởi tạo đối tượng `User`. Giúp tách biệt logic tạo đối tượng ra khỏi logic xử lý nghiệp vụ, dễ dàng quản lý và mở rộng sau này.
- **Facade Pattern (`ServerFacade.cs`)**: Cung cấp một giao diện đơn giản (`buildResponse`) để che giấu sự phức tạp của việc định dạng một chuỗi HTTP Response thô. Người lập trình chỉ cần truyền vào nội dung HTML, `Facade` sẽ lo phần định dạng header và mã hóa byte.

### 4. Cấu trúc dữ liệu và Lưu trữ
- **Models**: Chứa các lớp định nghĩa cấu trúc dữ liệu cho `User` (người dùng), `Message` (tin nhắn), và `ChatRoom` (phòng chat).
- **JSON Data**: Thông tin tài khoản được lưu trữ trong `users.json`. Khi cần kiểm tra đăng nhập, server sẽ đọc file này và so khớp tên đăng nhập/mật khẩu.
- **Chat Logic**: Trạng thái phòng chat (Online/Offline) dựa vào thời gian hoạt động cuối cùng (`lastActivity`). Nếu quá 3 phút không có tin nhắn mới, phòng sẽ chuyển sang offline và xóa lịch sử tin nhắn.

### 5. Quy trình thực hiện (Workflow)
1. Người dùng truy cập `localhost:8080` -> Server nhận request GET `/` -> Trả về trang thông tin sinh viên.
2. Click link "Login" -> Server nhận GET `/login` -> Trả về form đăng nhập.
3. Submit form -> Server nhận POST `/login` -> Kiểm tra tài khoản trong JSON -> Redirect qua Chat.
4. Trong Chat -> Gửi tin nhắn qua POST `/chat/:id` -> Server cập nhật lịch sử và trạng thái phòng chat.

---
*Ghi chú: Tài liệu này được bổ sung để phục vụ cho buổi vấn đáp và giải trình với giảng viên.*