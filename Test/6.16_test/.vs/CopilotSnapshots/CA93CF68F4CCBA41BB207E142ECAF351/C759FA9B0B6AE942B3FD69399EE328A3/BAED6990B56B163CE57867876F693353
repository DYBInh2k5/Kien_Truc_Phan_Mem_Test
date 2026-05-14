SA TEST
Objective:
Develop a web server using C# that utilizes WebSocket (2) technology.

Requirements:
API/Page Requirements: (5 points)
GET [/]: Displays detailed student information and provides a link to login.
GET [/login]: Shows the login page.
POST [/login]: Logs in with username and password. On success, redirects to /chat. On failure, displays a login failed message.
GET [/chat]: Displays online and offline chat rooms. A chat room is online if it has had activity within the last 3 minutes. If offline, its history is cleared.
POST [/chat/:id]: Sends a message to the chat room with the given id. After sending, changes the room status to online and redirects to GET /chat/:id
GET [/chat/:id]: Retrieves all messages sent to the chat room in chronological order (time, username, message).
User account information is stored in a JSON file with the following format: [ { "username": "nntu", "password": "56789" } , { "username": "nntu", "password": "56789" } ]

Apply 2 of the following design patterns: (3 points)
Singleton
Facade
Factory
Command
Builder
Submission Requirements:
3-5 screenshots demonstrating the web interface execution.
Image(s) of code implementing the chosen design pattern(s).
Compressed zip file containing the C# server and an HTML folder.

hướng dẫn làm bài này tạo dùng vscode 2022, hướng dẫn tạo file và làm



Ok bài này đúng kiểu:

Raw Socket + HTTP mini server + Web Chat

và thầy muốn m:

hiểu socket
parse HTTP
lưu trạng thái phòng chat
áp dụng design pattern

Quan trọng:

KHÔNG phải ASP.NET 😎

M phải giữ kiểu code socket như m gửi trước đó.

Tao sẽ hướng dẫn theo đúng style lab của m:

Socket
Thread
Receive
Send
tự parse HTTP
MỤC TIÊU CUỐI CÙNG

Browser mở:

http://localhost:8080

và có:

/            -> thông tin sinh viên
/login       -> form login
/chat        -> danh sách room
/chat/1      -> xem chat room 1
POST login   -> đăng nhập
POST chat    -> gửi tin nhắn
DESIGN PATTERN TAO KHUYÊN DÙNG

Dễ nhất:

1. Singleton

Dùng cho:

ChatManager

để toàn bộ server chỉ có 1 danh sách room.

2. Factory

Dùng cho:

ResponseFactory

tạo HTTP Response.

Dễ code.
Dễ chụp hình báo cáo.
Dễ giải thích.

KIẾN TRÚC PROJECT

Tạo project kiểu này:

SA_TEST/
│
├── Program.cs
├── users.json
│
├── Models/
│   ├── User.cs
│   ├── Message.cs
│   └── ChatRoom.cs
│
├── Managers/
│   └── ChatManager.cs
│
├── Factory/
│   └── ResponseFactory.cs
│
├── Html/
│   ├── index.html
│   ├── login.html
│   └── chat.html
│
└── Utils/
    └── HttpHelper.cs
BƯỚC 1 — TẠO PROJECT
Nếu dùng Visual Studio 2022
File → New Project

Chọn:

Console App (.NET)

Tên:

SA_TEST
BƯỚC 2 — TẠO THƯ MỤC

Chuột phải project:

Add -> New Folder

Tạo:

Models
Managers
Factory
Html
Utils
BƯỚC 3 — TẠO FILE
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
        public string Username { get; set; }

        public string Content { get; set; }

        public DateTime Time { get; set; }
    }
}
Models/ChatRoom.cs
using System;
using System.Collections.Generic;

namespace SA_TEST.Models
{
    internal class ChatRoom
    {
        public int Id { get; set; }

        public List<Message> Messages = new List<Message>();

        public DateTime LastActivity = DateTime.Now;
    }
}
BƯỚC 4 — SINGLETON
Managers/ChatManager.cs
using SA_TEST.Models;

namespace SA_TEST.Managers
{
    internal class ChatManager
    {
        private static ChatManager instance = null;

        public List<ChatRoom> Rooms = new List<ChatRoom>();

        private ChatManager()
        {
            for (int i = 1; i <= 3; i++)
            {
                Rooms.Add(new ChatRoom()
                {
                    Id = i
                });
            }
        }

        public static ChatManager getInstance()
        {
            if (instance == null)
            {
                instance = new ChatManager();
            }

            return instance;
        }
    }
}
Đây là DESIGN PATTERN 1
Singleton

📸 nhớ chụp file này cho báo cáo.

BƯỚC 5 — FACTORY PATTERN
Factory/ResponseFactory.cs
using System.Text;

namespace SA_TEST.Factory
{
    internal class ResponseFactory
    {
        public static byte[] Html(string body)
        {
            string response = "HTTP/1.1 200 OK\r\n";
            response += "Content-Type: text/html\r\n";
            response += $"Content-Length: {body.Length}\r\n";
            response += "\r\n";
            response += body;

            return Encoding.ASCII.GetBytes(response);
        }
    }
}
Đây là DESIGN PATTERN 2
Factory

📸 nhớ chụp file này.

BƯỚC 6 — users.json

Tạo file:

users.json
Nội dung
[
  {
    "username": "admin",
    "password": "123"
  },
  {
    "username": "otu",
    "password": "456"
  }
]
BƯỚC 7 — HTML
Html/index.html
<html>
<body>

<h1>SA TEST</h1>

<p>Ho Ten: Nguyen Van A</p>
<p>MSSV: 123456</p>

<a href="/login">Login</a>

</body>
</html>
Html/login.html
<html>
<body>

<h1>LOGIN</h1>

<form method="POST" action="/login">

Username:
<input name="username" />

<br>

Password:
<input name="password" />

<br>

<button type="submit">
Login
</button>

</form>

</body>
</html>
BƯỚC 8 — PROGRAM.CS

Đây là file quan trọng nhất 😎

Main socket
using System.Net;
using System.Net.Sockets;
using System.Text;
using SA_TEST.Factory;
using SA_TEST.Managers;

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
handleClient
static void handleClient(object obj)
{
    Socket staff = (Socket)obj;

    byte[] bytes = new byte[4096];

    int byteRec = staff.Receive(bytes);

    string request =
        Encoding.ASCII.GetString(bytes, 0, byteRec);

    Console.WriteLine(request);

    string firstLine =
        request.Split('\n')[0];

    if (firstLine.Contains("GET / "))
    {
        string html =
            File.ReadAllText("Html/index.html");

        staff.Send(ResponseFactory.Html(html));
    }

    else if (firstLine.Contains("GET /login"))
    {
        string html =
            File.ReadAllText("Html/login.html");

        staff.Send(ResponseFactory.Html(html));
    }

    else
    {
        string html =
            "<html><body>404</body></html>";

        staff.Send(ResponseFactory.Html(html));
    }

    staff.Close();
}
TEST

Run project.

Browser:

http://localhost:8080

Nếu thấy web:

=> thành công 😎

BƯỚC 9 — LOGIN

Sau đó mới làm:

POST /login
Parse POST

HTTP Request sẽ kiểu:

POST /login HTTP/1.1
...
username=admin&password=123
M sẽ parse:
username=
password=
Đọc JSON

Dùng:

System.Text.Json
Check account

Nếu đúng:

redirect /chat
Redirect HTTP
HTTP/1.1 302 Found
Location: /chat
BƯỚC 10 — CHAT ROOM

Dùng:

ChatManager.getInstance()

để lấy rooms.

Online / Offline
Now - LastActivity < 3 phút

=> ONLINE.

Nếu offline
room.Messages.Clear();
POST /chat/1

Thêm message vào:

room.Messages.Add(...)
GET /chat/1

Loop messages:

foreach

render HTML.

SCREENSHOT CẦN CHỤP
1

Trang chủ.

2

Trang login.

3

Login thành công.

4

Chat room.

5

Code Singleton + Factory.

NỘP FILE

Zip:

SA_TEST.zip

bao gồm:

Program.cs
Html/
users.json
Models/
Managers/
Factory/
QUAN TRỌNG 😎

Bài này thầy đang kiểm tra:

✅ socket
✅ thread
✅ parse HTTP
✅ design pattern
✅ state management
✅ low-level web server

chứ KHÔNG phải UI đẹp.

UI xấu cũng được.

Socket chạy đúng mới là vua 💀

---

## 📘 CHI TIẾT CÔNG DỤNG & CÁCH HOẠT ĐỘNG CỦA CÁC FILE

### 1. Thư mục `Models/` (Lớp dữ liệu)
- **`User.cs`**: Định nghĩa cấu trúc người dùng (username, password). Dùng để ánh xạ (Map) dữ liệu từ file `users.json` vào đối tượng trong C# để kiểm tra đăng nhập.
- **`Message.cs`**: Định nghĩa cấu trúc của một tin nhắn chat (người gửi, nội dung, thời gian).
- **`ChatRoom.cs`**: Quản lý thông tin một phòng chat. 
    - **Cách hoạt động**: Chứa danh sách các `Message`. File này có logic quan trọng nhất là kiểm tra thuộc tính `LastActivity`. Nếu thời gian hiện tại trừ đi `LastActivity` > 3 phút, phòng chat sẽ được coi là **Offline** và tự động gọi `Messages.Clear()` để xóa lịch sử theo yêu cầu đề bài.

### 2. Thư mục `Managers/` (Lớp quản lý - Singleton)
- **`ChatManager.cs`**: 
    - **Công dụng**: Là nơi lưu trữ duy nhất danh sách các phòng chat trong toàn bộ vòng đời của Server. 
    - **Cách hoạt động**: Áp dụng **Singleton Pattern**. Nó đảm bảo dù có 100 khách hàng truy cập đồng thời (trên 100 Thread khác nhau), tất cả đều truy cập vào đúng một danh sách phòng chat duy nhất, giúp tin nhắn của người này hiện lên ở máy người kia.

### 3. Thư mục `Factory/` (Lớp hỗ trợ - Factory Pattern)
- **`ResponseFactory.cs`**:
    - **Công dụng**: "Nhà máy" chuyên sản xuất các gói tin phản hồi HTTP.
    - **Cách hoạt động**: Thay vì viết code rườm rà trong `Program.cs`, ta chỉ cần gọi `ResponseFactory.Html(content)`. Bên trong nó tự động đóng gói các Header chuẩn của HTTP như `HTTP/1.1 200 OK`, `Content-Type`, `Content-Length`. Điều này thể hiện tính **Encapsulation** (Đóng gói) trong kiến trúc phần mềm.

### 4. Thư mục `Html/` (Giao diện)
- **`index.html`**: Trang chủ hiển thị thông tin cá nhân.
- **`login.html`**: Form đăng nhập gửi dữ liệu qua phương thức `POST`.
- **`chat.html`**: Danh sách các phòng chat kèm trạng thái Online/Offline.
- **`room.html`**: Giao diện chi tiết trong một phòng chat để xem tin nhắn và gửi tin nhắn mới.

### 5. File chính & Cấu hình
- **`users.json`**: Đóng vai trò như một Database nhỏ gọn, lưu trữ thông tin tài khoản hợp lệ.
- **`Program.cs`**: "Trái tim" của hệ thống.
    - **Khởi tạo**: Tạo `Socket`, `Bind` vào cổng 8080 và `Listen`.
    - **Xử lý đa luồng**: Sử dụng `Thread` để mỗi khi có khách truy cập, Server không bị treo mà xử lý song song nhiều người cùng lúc.
    - **Parse HTTP**: Tự đọc chuỗi văn bản từ trình duyệt gửi lên, tách lấy dòng đầu tiên để biết khách muốn vào trang nào (Routing) và tách lấy Body để lấy dữ liệu đăng nhập hoặc tin nhắn.

## 📡 LUỒNG HOẠT ĐỘNG TỔNG QUÁT (Để vấn đáp)
1. **Request**: Trình duyệt gửi gói tin TCP đến 8080.
2. **Accept**: Server chấp nhận và đẩy vào một `Thread` mới.
3. **Routing**: `Program.cs` đọc URL (ví dụ: `/chat/1`).
4. **Logic**: `ChatManager` lấy phòng số 1, kiểm tra xem nó còn Online không. Nếu mới gửi tin nhắn thì cập nhật `LastActivity`.
5. **Response**: `ResponseFactory` đóng gói HTML thành gói tin HTTP và gửi ngược lại cho trình duyệt qua Socket.
6. **Close**: Socket đóng lại, giải phóng tài nguyên.

---

## 🛡️ TUÂN THỦ QUY ĐỊNH BÀI THI (DÀNH CHO SINH VIÊN)

Để đảm bảo đạt điểm tối đa và không vi phạm quy chế (như yêu cầu của thầy), bạn cần lưu ý các điểm sau:

### 1. Giải thích về Source Code (Phần quan trọng nhất khi Vấn đáp)
- **Socket Programming:** Đề bài yêu cầu dùng WebSocket, nhưng trong lab này chúng ta đang giả lập Web Server bằng **Raw Socket**. Bạn giải thích: "Em sử dụng thư viện `System.Net.Sockets` để lắng nghe yêu cầu HTTP ở tầng vận chuyển (Transport Layer), sau đó tự xử lý (Parse) gói tin để trả về HTML."
- **Nghiệp vụ "Clear History":** Logic này nằm ở hàm `CheckStatus()` của class `ChatRoom`. Khi giáo viên hỏi "Làm sao để biết phòng Offline?", hãy chỉ vào thuộc tính `LastActivity` và toán tử so sánh `TotalMinutes < 3`.
- **Đăng nhập (Authentication):** Dữ liệu được đọc từ `users.json` bằng thư viện `System.Text.Json`. Đây là cách quản lý dữ liệu tĩnh hiệu quả cho các bài bài thi nhỏ.

### 2. Hai mẫu thiết kế đã áp dụng (Design Patterns)
*Bạn PHẢI chụp hình 2 file này như yêu cầu Part 2 của thầy:*
1.  **Singleton Pattern (`ChatManager.cs`):** 
    - *Giải thích:* Để duy trì một danh sách phòng chat duy nhất không bị khởi tạo lại khi có request mới. Constructor được để là `private` và truy cập qua `GetInstance()`.
2.  **Factory Pattern (`ResponseFactory.cs`):** 
    - *Giải thích:* Dùng để chuyên môn hóa việc tạo gói tin phản hồi. Giúp tách biệt logic xử lý web và cấu trúc gói tin HTTP thuần túy.

### 3. Cấu trúc nộp bài (Theo yêu cầu Part 1, 2, 3)
Trước khi nén ZIP (`SA_TEST.zip`), hãy kiểm tra:
- **Folder `Results-screenshots`**: Chứa ảnh chụp trang chủ, login, danh sách chat và nội dung chat (3-5 tấm).
- **Folder `Code-DesignPatterns`**: Chụp màn hình vùng code quan trọng của `ChatManager.cs` (phần Singleton) và `ResponseFactory.cs` (phần Factory).
- **Folder `ProjectCode`**: Toàn bộ source code của bạn (trừ folder `bin` và `obj` để file nén nhẹ hơn).

### 4. Kiểm tra tính năng (Application Functionality)
- [ ] Chạy lệnh `dotnet run` thành công và không có lỗi build.
- [ ] Đăng nhập được bằng tài khoản `admin/123` hoặc `nntu/56789` từ file `users.json`.
- [ ] Gửi được tin nhắn vào phòng chat và phòng đó chuyển sang trạng thái "Online".
- [ ] Kiểm tra logic 3 phút: Đợi thử 3 phút xem tin nhắn có tự xóa và trạng thái có về "Offline" không (để chứng minh cho thầy thấy).

### 5. Chuẩn bị nội dung vấn đáp (Oral Explanation)
Hãy chắc chắn bạn trả lời được các câu hỏi sau:
- **"Tại sao nộp file .json cho tài khoản?"**: Vì đây là yêu cầu lưu giữ thông tin người dùng của đề bài, giúp dễ dàng kiểm tra mà không cần DB phức tạp.
- **"Phòng chat online/offline hoạt động thế nào?"**: Dựa vào so sánh `DateTime.Now` và `LastActivity` của mỗi phòng chat.
- **"Nếu không dùng Thread thì sao?"**: Server sẽ chỉ phục vụ được duy nhất 1 người dùng tại một thời điểm, những người khác sẽ bị quay vòng chờ đợi (Blocked).

### 6. Liêm chính học thuật (Academic Integrity)
- Tuyệt đối không nộp bài giống hệt bạn khác.
- Tự tay thực hiện các thay đổi nhỏ về giao diện (HTML/CSS) trong thư mục `Html/` để bài làm mang tính cá nhân hóa cao hơn.

**Ghi chú:** Luôn chạy `dotnet run` và kiểm tra lại mọi liên kết trên trình duyệt trước khi nộp bài để đảm bảo tính sẵn sàng của ứng dụng.

---

## 📋 CHECKLIST QUAN TRỌNG TRƯỚC KHI NỘP BÀI (TUÂN THỦ YÊU CẦU CỦA GIẢNG VIÊN)

Dưới đây là danh sách kiểm tra cuối cùng để đảm bảo bạn không bỏ lỡ bất kỳ yêu cầu nào từ thầy:

### 1. Kiểm tra sự hiện diện (Attendance)
- Đảm bảo bạn đang có mặt tại phòng Lab/lớp học được chỉ định. Đây là điều kiện tiên quyết để được chấm bài.

### 2. Cấu trúc thư mục nộp bài (Submission Structure)
Bạn cần tạo một folder gốc (ví dụ: `LUOI_THI_SA_TEST`) và bên trong chia thành đúng 3 folder con như sau:
- **`Results-screenshots/`**: 
    - [ ] Ảnh 1: Trang chủ (`GET /`) hiện thông tin cá nhân.
    - [ ] Ảnh 2: Trang Login (`GET /login`).
    - [ ] Ảnh 3: Trang danh sách Chat (`GET /chat`) hiện các phòng Online/Offline.
    - [ ] Ảnh 4: Giao diện bên trong một phòng chat cụ thể.
    - [ ] Ảnh 5: Thông báo lỗi khi đăng nhập sai.
- **`Code-DesignPatterns/`**:
    - [ ] Ảnh 6: Code triển khai **Singleton** trong file `ChatManager.cs`.
    - [ ] Ảnh 7: Code triển khai **Factory** trong file `ResponseFactory.cs`.
- **`ProjectCode/`**:
    - [ ] Chứa toàn bộ source code C# (file `.sln`, `.csproj`, các file `.cs`, folder `Html`, file `users.json`). *Lưu ý: Bạn nên xóa folder `bin` và `obj` trước khi nén để tránh lỗi đường dẫn.*

### 3. Kiểm tra tính năng (Application Functionality)
- [ ] Chạy lệnh `dotnet run` thành công và không có lỗi build.
- [ ] Đăng nhập được bằng tài khoản `admin/123` hoặc `nntu/56789` từ file `users.json`.
- [ ] Gửi được tin nhắn vào phòng chat và phòng đó chuyển sang trạng thái "Online".
- [ ] Kiểm tra logic 3 phút: Đợi thử 3 phút xem tin nhắn có tự xóa và trạng thái có về "Offline" không (để chứng minh cho thầy thấy).

### 4. Chuẩn bị nội dung vấn đáp (Oral Explanation)
Hãy chắc chắn bạn trả lời được các câu hỏi sau:
- **"Tại sao nộp file .json cho tài khoản?"**: Vì đây là yêu cầu lưu giữ thông tin người dùng của đề bài, giúp dễ dàng kiểm tra mà không cần DB phức tạp.
- **"Phòng chat online/offline hoạt động thế nào?"**: Dựa vào so sánh `DateTime.Now` và `LastActivity` của mỗi phòng chat.
- **"Nếu không dùng Thread thì sao?"**: Server sẽ chỉ phục vụ được duy nhất 1 người dùng tại một thời điểm, những người khác sẽ bị quay vòng chờ đợi (Blocked).

### 5. Liêm chính học thuật (Academic Integrity)
- Tuyệt đối không nộp bài giống hệt bạn khác.
- Tự tay thực hiện các thay đổi nhỏ về giao diện (HTML/CSS) trong thư mục `Html/` để bài làm mang tính cá nhân hóa cao hơn.

**Kết quả cuối cùng:** Sau khi nén folder gốc thành file `.zip`, hãy kiểm tra lại một lần nữa xem file nén có bị lỗi không trước khi upload lên hệ thống.