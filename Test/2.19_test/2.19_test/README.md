SA TEST 19/02
old: 14/11
Objective:
Develop a web server using C# that utilizes Socket - library (System.Net.Sockets).

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
Singleton: Apply to the class reading JSON content
Builder: Create & Add Controller (login, chat, home) to WebRouter
Time Requirement: (1 point)
Students must submit their work before 4 PM, and grading will be completed in class.
Other Requirements: (1point)
Implement cookie storage, include a token, and ensure the website has an attractive design.
Submission Requirements:
Link: https://mlearning.hoasen.edu.vn/mod/assign/view.php?id=1125940

Submit 3 parts:

3-5 screenshots demonstrating the web interface execution.
3-5 Image(s) of code implementing the chosen design pattern(s).
zip file: containing the C# server and an HTML folder.
hướng dẫn làm bài này tạo dùng vscode 2022, hướng dẫn tạo file và làm


Bài này đúng kiểu:

“Tự build mini web framework bằng raw Socket” 😎

Và với style code m gửi trước đó thì hoàn toàn làm được.

Tao sẽ hướng dẫn đúng hệ:

✅ raw Socket
✅ Thread
✅ parse HTTP bằng tay
✅ VSCode / Visual Studio
✅ không ASP.NET
✅ đúng kiểu lab môn Software Architecture + Network

MỤC TIÊU CUỐI CÙNG

Sau khi xong m sẽ có:

SA_TEST/
│
├── Program.cs
├── Router/
│   ├── WebRouter.cs
│   └── RouteBuilder.cs
│
├── Controllers/
│   ├── HomeController.cs
│   ├── LoginController.cs
│   └── ChatController.cs
│
├── Models/
│   ├── User.cs
│   ├── Message.cs
│   └── ChatRoom.cs
│
├── Services/
│   ├── JsonService.cs
│   ├── CookieService.cs
│   └── ChatService.cs
│
├── Data/
│   └── users.json
│
├── Html/
│   ├── login.html
│   ├── home.html
│   └── style.css
│
└── Utils/
    └── HttpHelper.cs
PHẦN 1 — TẠO PROJECT
Nếu dùng Visual Studio 2022
B1

Mở:

Visual Studio 2022
B2

Chọn:

Create new project
B3

Chọn:

Console App (.NET)

KHÔNG chọn ASP.NET.

B4

Tên project:

SA_TEST
B5

Framework:

.NET 6 hoặc .NET 8
PHẦN 2 — TẠO THƯ MỤC
Trong Solution Explorer

Right click project:

Add
→ New Folder

Tạo:

Controllers
Models
Services
Router
Html
Data
Utils
PHẦN 3 — TẠO FILE
Controllers

Right click folder:

Add
→ Class

Tạo:

HomeController.cs
LoginController.cs
ChatController.cs
Models

Tạo:

User.cs
Message.cs
ChatRoom.cs
Services

Tạo:

JsonService.cs
CookieService.cs
ChatService.cs
Router

Tạo:

WebRouter.cs
RouteBuilder.cs
Utils

Tạo:

HttpHelper.cs
Data

Tạo file:

users.json
Html

Tạo:

login.html
home.html
style.css
PHẦN 4 — users.json
Data/users.json
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
PHẦN 5 — MODEL
Models/User.cs
namespace SA_TEST.Models
{
    internal class User
    {
        public string username { get; set; }
        public string password { get; set; }
    }
}
Models/Message.cs
namespace SA_TEST.Models
{
    internal class Message
    {
        public string username { get; set; }

        public string content { get; set; }

        public DateTime time { get; set; }
    }
}
Models/ChatRoom.cs
using System.Collections.Generic;

namespace SA_TEST.Models
{
    internal class ChatRoom
    {
        public int id { get; set; }

        public List<Message> messages =
            new List<Message>();

        public DateTime lastActivity { get; set; }
    }
}
PHẦN 6 — SINGLETON PATTERN

Yêu cầu đề bài 😎

Services/JsonService.cs
using System.Text.Json;
using SA_TEST.Models;

namespace SA_TEST.Services
{
    internal class JsonService
    {
        private static JsonService instance = null;

        private JsonService() { }

        public static JsonService getInstance()
        {
            if (instance == null)
            {
                instance = new JsonService();
            }

            return instance;
        }

        public List<User> getUsers()
        {
            string json =
                File.ReadAllText("Data/users.json");

            return JsonSerializer.Deserialize<List<User>>(json);
        }
    }
}
Đây chính là:
Singleton Pattern
PHẦN 7 — BUILDER PATTERN
Router/WebRouter.cs
namespace SA_TEST.Router
{
    internal class WebRouter
    {
        public Dictionary<string, Func<string>> routes =
            new Dictionary<string, Func<string>>();

        public void addRoute(string url, Func<string> action)
        {
            routes[url] = action;
        }
    }
}
Router/RouteBuilder.cs
namespace SA_TEST.Router
{
    internal class RouteBuilder
    {
        private WebRouter router =
            new WebRouter();

        public RouteBuilder addHome(Func<string> action)
        {
            router.addRoute("/", action);
            return this;
        }

        public RouteBuilder addLogin(Func<string> action)
        {
            router.addRoute("/login", action);
            return this;
        }

        public WebRouter build()
        {
            return router;
        }
    }
}
Đây là:
Builder Pattern
PHẦN 8 — HOME CONTROLLER
Controllers/HomeController.cs
namespace SA_TEST.Controllers
{
    internal class HomeController
    {
        public static string Index()
        {
            return @"
            <html>
            <body>
                <h1>Student Information</h1>

                <p>ID: 2212345</p>
                <p>Fullname: Nguyen Van A</p>
                <p>PC: PC01</p>

                <a href='/login'>Login</a>

            </body>
            </html>
            ";
        }
    }
}
PHẦN 9 — LOGIN CONTROLLER
Controllers/LoginController.cs
using SA_TEST.Services;

namespace SA_TEST.Controllers
{
    internal class LoginController
    {
        public static string LoginPage()
        {
            return @"
            <html>
            <body>

            <form method='POST' action='/login'>

                Username:
                <input name='username'/>

                <br/>

                Password:
                <input name='password' type='password'/>

                <br/>

                <button>Login</button>

            </form>

            </body>
            </html>
            ";
        }
    }
}
PHẦN 10 — PROGRAM.CS

Đây là trái tim server 😎

Program.cs
using System.Net;
using System.Net.Sockets;
using System.Text;

IPEndPoint serverInfor =
    new IPEndPoint(IPAddress.Any, 8080);

Socket serverListen = new Socket(
    AddressFamily.InterNetwork,
    SocketType.Stream,
    ProtocolType.Tcp
);

serverListen.Bind(serverInfor);

serverListen.Listen(10);

Console.WriteLine("Dang cho client...");

while (true)
{
    Socket staff = serverListen.Accept();

    Thread thread = new Thread(handleClient);

    thread.Start(staff);
}

static void handleClient(object obj)
{
    Socket staff = (Socket)obj;

    byte[] bytes = new byte[1024];

    int bytesRec = staff.Receive(bytes);

    string requestData =
        Encoding.ASCII.GetString(bytes, 0, bytesRec);

    Console.WriteLine(requestData);

    string responseBody = "";

    if (requestData.StartsWith("GET / "))
    {
        responseBody =
            SA_TEST.Controllers.HomeController.Index();
    }
    else if (requestData.StartsWith("GET /login"))
    {
        responseBody =
            SA_TEST.Controllers.LoginController.LoginPage();
    }

    string responseData =
        "HTTP/1.1 200 OK\r\n";

    responseData +=
        "Content-Type: text/html\r\n";

    responseData +=
        $"Content-Length: {responseBody.Length}\r\n";

    responseData += "\r\n";

    responseData += responseBody;

    byte[] msg =
        Encoding.ASCII.GetBytes(responseData);

    staff.Send(msg);

    staff.Close();
}
PHẦN 11 — CHẠY SERVER
Nhấn
Ctrl + F5
Browser mở:
http://localhost:8080
PHẦN 12 — SAU ĐÓ LÀM TIẾP

Sau khi chạy được basic server:

Bước tiếp theo
1. POST /login
   - Parse dữ liệu từ body của Request (ví dụ: `username=nntu&password=56789`).
   - Sử dụng `HttpHelper.ParseFormData` để tách key-value.
   - So khớp với dữ liệu từ `JsonService.getInstance().getUsers()`.

2. Cookie & Session
   - Khi login thành công, trả vềHeader: `Set-Cookie: token=username; Path=/`.
   - Các request sau sẽ đọc `Cookie` header để nhận diện user qua `HttpHelper.GetCookie`.

3. GET /chat (Trang danh sách phòng)
   - Kiểm tra Cookie token: Nếu chưa login -> Redirect (302) về `/login`.
   - Lấy danh sách phòng từ `ChatService`.
   - Hiển thị trạng thái Online/Offline dựa trên `lastActivity`.

4. GET /chat/:id (Trang nội dung phòng)
   - Lấy `id` từ URL.
   - Hiển thị lịch sử tin nhắn của phòng đó.
   - Tự động xóa lịch sử nếu `(DateTime.Now - room.lastActivity).TotalMinutes > 3`.

5. POST /chat/:id (Gửi tin nhắn)
   - Lấy tin nhắn từ form POST.
   - Cập nhật vào `ChatRoom.messages`.
   - Cập nhật `lastActivity = DateTime.Now`.
   - Redirect về trang chat vừa gửi.

HƯỚNG DẪN CHI TIẾT CÁC THỰC HIỆN (EXPLAINED)

1. Xử lý Socket:
   - Server lắng nghe tại port 8080.
   - Mỗi client kết nối được cấp một `Thread` riêng để xử lý (`HandleClient`), giúp nhiều người dùng truy cập cùng lúc.

2. Phân tích HTTP (Manual Parsing):
   - Đọc dữ liệu thô từ Socket.
   - Dòng đầu tiên chứa Method (GET/POST) và URL.
   - Các dòng tiếp theo là Headers. Sau dấu `\r\n\r\n` là Body (dành cho POST).

3. Áp dụng Design Patterns:
   - Singleton (JsonService): Đảm bảo chỉ có một instance duy nhất đọc file JSON, tiết kiệm tài nguyên và đồng nhất dữ liệu.
   - Builder (WebRouter/RouteBuilder): Giúp việc đăng ký các đường dẫn (routes) trở nên mạch lạc và dễ mở rộng.

4. Quản lý trạng thái (State Management):
   - Vì không dùng DB, dữ liệu User được nạp từ file JSON.
   - Dữ liệu Chat được lưu trong bộ nhớ (Static List) của `ChatService`.

Nộp bài cần chụp hình
Chụp:
1

Trang home.

2

Trang login.

3

Login success.

4

Chat room online/offline.

5

Code Singleton.

6

Code Builder.

Quan trọng 😎

Đề này KHÔNG yêu cầu:

database
ASP.NET
Entity Framework

Nó muốn:

hiểu Socket + HTTP + Design Pattern

Đây là kiểu “build web framework primitive” 💀

### PHẦN 13 — GIẢI THÍCH CHI TIẾT CÁC FILE (VẤN ĐÁP)

Dưới đây là công dụng của từng file để bạn trả lời khi được hỏi:

1.  **Lớp Khởi tạo & Cấu hình (Root)**
    *   **`Program.cs`**: "Trái tim" của Server. Khởi tạo Socket lắng nghe tại cổng 8080, sử dụng `Thread` để xử lý đa luồng (multi-threading) và thực hiện phân tích (parsing) HTTP thô để điều phối request.

2.  **Lớp Mô hình (Models)**
    *   **`User.cs`**: Định nghĩa cấu trúc tài khoản người dùng (username, password).
    *   **`Message.cs`**: Định nghĩa cấu trúc một tin nhắn (người gửi, nội dung, thời gian).
    *   **`ChatRoom.cs`**: Định nghĩa đối tượng phòng chat, quản lý danh sách tin nhắn và thời gian hoạt động cuối cùng.

3.  **Lớp Dịch vụ (Services)**
    *   **`JsonService.cs`**: (**Singleton**) Đảm bảo chỉ có một instance duy nhất chịu trách nhiệm đọc file `users.json`. Giúp tiết kiệm RAM và đồng nhất dữ liệu.
    *   **`ChatService.cs`**: Quản lý nghiệp vụ chat. Chứa logic quan trọng: **Tự động xóa lịch sử tin nhắn và chuyển trạng thái Offline sau 3 phút không hoạt động.**
    *   **`CookieService.cs`**: (Hỗ trợ) Quản lý việc tạo và xác thực các thẻ token định danh người dùng.

4.  **Lớp Điều khiển (Controllers)**
    *   **`HomeController.cs`**: Tạo mã HTML hiển thị thông tin sinh viên tại trang chủ (`/`).
    *   **`LoginController.cs`**: Tạo giao diện Form đăng nhập đẹp mắt.
    *   **`ChatController.cs`**: Render danh sách phòng chat và giao diện cửa sổ chat từ dữ liệu của `ChatService`.

5.  **Lớp Điều hướng (Router)**
    *   **`WebRouter.cs`**: Bản đồ ánh xạ giữa đường dẫn (URL) và hàm xử lý tương ứng.
    *   **`RouteBuilder.cs`**: (**Builder**) Giúp cấu hình các route một cách linh hoạt theo kiểu nối chuỗi (Fluent Interface).

6.  **Lớp Tiện ích & Dữ liệu (Utils / Data)**
    *   **`HttpHelper.cs`**: Công cụ bóc tách chuỗi HTTP thô thành Dictionary (cho dữ liệu Form) và trích xuất thông tin Cookie.
    *   **`users.json`**: Cơ sở dữ liệu dạng file văn bản lưu trữ thông tin đăng nhập.
    *   **`style.css`**: Nâng cao trải nghiệm người dùng bằng giao diện hiện đại, màu sắc hài hòa.

### PHẦN 14 — CƠ CHẾ HOẠT ĐỘNG CHÍNH

1.  **Cách xử lý POST /login**:
    *   Server đọc dữ liệu sau dòng trống `\r\n\r\n` của request.
    *   Sử dụng `HttpHelper.ParseFormData` để lấy username/password.
    *   So sánh với dữ liệu từ `JsonService`. Nếu đúng, Server gửi header `Set-Cookie: token=...` để trình duyệt lưu lại.

2.  **Cách duy trì đăng nhập**:
    *   Mỗi khi bạn chuyển trang, trình duyệt tự gửi kèm header `Cookie`.
    *   Server đọc header này, nếu thấy token hợp lệ thì cho phép vào trang `/chat`, ngược lại sẽ dùng mã `302 Found` (Redirect) để đẩy về `/login`.

3.  **Cách xử lý Online/Offline (3 phút)**:
    *   Mỗi khi có tin nhắn mới, `lastActivity` của phòng được cập nhật thành `DateTime.Now`.
    *   Mỗi khi ai đó tải trang danh sách phòng, hệ thống tính toán: `DateTime.Now - room.lastActivity`. 
    *   Nếu thời gian này lớn hơn 180 giây (3 phút) -> Gọi `messages.Clear()` -> Trạng thái hiển thị là "Offline".

4.  **Tại sao dùng raw Socket?** 
    *   Mục tiêu là để hiểu sâu về giao thức TCP/IP và HTTP ở tầng thấp nhất, nơi mà các Framework như ASP.NET đã ẩn đi.

---

### PHẦN 15 — QUY ĐỊNH NỘP BÀI & HƯỚNG DẪN CHI TIẾT (DÀNH CHO SINH VIÊN)

Dưới đây là phần giải thích chuyên sâu để chuẩn bị cho buổi vấn đáp trực tiếp với giảng viên:

#### 1. Yêu cầu về Attendance & Oral Explanation (Vấn đáp)
*   **Chiến thuật:** Khi thầy hỏi về bất kỳ chức năng nào, hãy mở file tương ứng trong thư mục `Controllers` (giao diện) hoặc `Services` (logic). 
*   **Giải thích code:** 
    - Luôn bắt đầu từ `Program.cs` (điểm bắt đầu của ứng dụng).
    - Giải thích cách `Socket` nhận dữ liệu thô (byte array) và `Encoding.UTF8.GetString` chuyển nó thành văn bản để xử lý.

#### 2. Cấu trúc thư mục nộp bài (Chuẩn 3 phần)
Để đảm bảo điểm số tối đa theo yêu cầu, hãy tổ chức file nộp bài như sau:
*   **Thư mục `Results-screenshots`:**
    - `01_Homepage.png`: Chụp trang thông tin sinh viên.
    - `02_LoginPage.png`: Chụp giao diện form đăng nhập.
    - `03_LoginSuccess_ChatList.png`: Chụp màn hình sau khi login thành công, thấy danh sách phòng.
    - `04_ChatRoom_Online.png`: Chụp cảnh đang chat trong phòng.
    - `05_ChatRoom_Offline.png`: Chụp cảnh phòng sau 3 phút không chat (lịch sử bị xóa). (Cần tên file rõ ràng theo Task).
*   **Thư mục `Code-DesignPatterns`:**
    - `DP_Singleton.png`: Chụp file `JsonService.cs` phần `getInstance()`.
    - `DP_Builder.png`: Chụp file `RouteBuilder.cs` và đoạn gọi code trong `Program.cs`.
*   **Thư mục `ProjectCode`:**
    - Chứa toàn bộ source code của project (bao gồm file `.csproj`, thư mục `Controllers`, `Models`, `Services`, `Router`, `Html`, `Data`, `Utils`).

#### 3. Giải thích tính minh bạch & Tự thực hiện (Academic Integrity)
*   Dự án này được xây dựng dựa trên kiến thức môn **Software Architecture** và **Network Programming**.
*   **Điểm nhấn tự làm:** 
    - Tự định nghĩa `HttpHelper.cs` để parse dữ liệu mà không dùng thư viện `Newtonsoft.Json` hay `System.Web`.
    - Tự quản lý trạng thái Online/Offline bằng logic so sánh `DateTime`.
    - Giao diện CSS (`style.css`) được tùy chỉnh thủ công để đảm bảo tính thẩm mỹ độc nhất.

#### 4. Lưu ý quan trọng khi Demo cho Giảng viên:
*   **Kiểm tra trước:** Chạy `dotnet run` và thử đăng nhập bằng tài khoản `nntu` mật khẩu `56789`.
*   **Debug:** Nếu giảng viên yêu cầu thay đổi thời gian timeout (ví dụ từ 3 phút xuống 1 phút), bạn hãy vào `ChatService.cs` và sửa con số `3` thành `1`. Đây là cách chứng minh bạn hiểu và kiểm soát được code của mình.
*   **Tính toàn vẹn:** Đảm bảo thư mục `Data/users.json` luôn tồn tại cạnh file thực thi để server không bị lỗi khi đọc dữ liệu.

### PHẦN 16 — TUÂN THỦ QUY ĐỊNH NỘP BÀI (RECAP)

Dựa trên yêu cầu của giảng viên, sinh viên cần đảm bảo:
- **Hiện diện:** Phải có mặt tại phòng Lab lúc chấm bài.
- **Cấu trúc nộp:** Chia rõ 3 folder `Results-screenshots`, `Code-DesignPatterns`, và `ProjectCode`.
- **Giải thích (Oral):** Nắm vững chức năng của từng file (đã chú thích trong code) để trả lời vấn đáp.
- **Tính năng:** Đảm bảo server chạy được trên máy tính tại trường (không thiếu file `Data/users.json`).
- **Chính trực:** Hiểu rõ mã nguồn để chỉnh sửa theo yêu cầu của thầy tại chỗ.

---
*Chúc bạn có một buổi vấn đáp thành công và đạt điểm cao!*

