Test (Coding)
Objective:

Develop a web server using C# that utilizes WebSocket technology.
Requirements:

RESTful Methods Support:
Implement RESTful methods such as GET, POST, DELETE, and PUT.
Basic Pages:
Create and handle two simple pages:
Login Page
Chat Page
Data Storage:

Store data in specified formats using text files (.txt) and JSON files (.json).
Ensure the web server can handle the specified RESTful requests and manage the login and chat functionalities effectively, with data persistence in the required formats.

hướng dẫn làm bài này tạo dùng vscode 2022, hướng dẫn tạo file và làm


Ok bài này bản chất là:

Web Server Socket + WebSocket + REST API mini bằng C#

Và theo style code m đang học thì tao sẽ giữ:

✅ raw Socket
✅ Thread
✅ tự parse HTTP
✅ không nhảy ASP.NET Core
✅ làm kiểu lab network/system

Mục tiêu bài này

M cần làm:

1. Web Server bằng Socket
2. Hỗ trợ:
   - GET
   - POST
   - PUT
   - DELETE

3. Có:
   - Login Page
   - Chat Page

4. Lưu dữ liệu:
   - .txt
   - .json

5. Có WebSocket chat realtime
Kiến trúc nên làm
Browser
   |
HTTP Request / WebSocket
   |
Socket Server
   |
------------------------
| REST Handler         |
| Login Handler        |
| Chat Handler         |
| File JSON/TXT        |
------------------------
Cấu trúc thư mục nên làm
W0606SocketWeb/
│
├── Program.cs
├── HttpHandler.cs
├── WebSocketHandler.cs
├── FileManager.cs
├── User.cs
│
├── data/
│   ├── users.json
│   └── chat.txt
│
├── pages/
│   ├── login.html
│   └── chat.html
BƯỚC 1 — Tạo project trong Visual Studio 2022
Mở Visual Studio 2022

Chọn:

Create a new project
Chọn
Console App (.NET)
Next

Tên project:

W0606SocketWeb
Chọn .NET
.NET 6 hoặc .NET 8
Create

Xong 😎

BƯỚC 2 — Tạo thư mục

Trong Solution Explorer:

Tạo folder
pages

Right Click project:

Add
→ New Folder
→ pages
data

Tạo thêm:

data
BƯỚC 3 — Tạo file HTML
login.html

Trong pages

Right Click:

Add
→ New Item
→ HTML Page

Tên:

login.html
Code login.html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>

    <h1>Login Page</h1>

    <form method="POST" action="/login">

        Username:
        <input type="text" name="username" />

        <br /><br />

        Password:
        <input type="password" name="password" />

        <br /><br />

        <button type="submit">
            Login
        </button>

    </form>

</body>
</html>
chat.html

Tạo tiếp:

chat.html
Code
<!DOCTYPE html>
<html>
<head>
    <title>Chat</title>
</head>
<body>

<h1>Chat Page</h1>

<input type="text" id="msg" />

<button onclick="sendMsg()">
    Send
</button>

<div id="chat"></div>

<script>

let ws =
new WebSocket("ws://localhost:8080/ws");

ws.onmessage = function(event)
{
    document.getElementById("chat").innerHTML +=
    "<p>" + event.data + "</p>";
};

function sendMsg()
{
    let msg =
    document.getElementById("msg").value;

    ws.send(msg);
}

</script>

</body>
</html>
BƯỚC 4 — Tạo User.cs
User.cs
internal class User
{
    public string username { get; set; }

    public string password { get; set; }
}
BƯỚC 5 — Tạo FileManager.cs
FileManager.cs
using System.Text.Json;

internal class FileManager
{
    public static void saveUser(User user)
    {
        string json =
            JsonSerializer.Serialize(user);

        File.AppendAllText(
            "data/users.json",
            json + "\n"
        );
    }

    public static void saveChat(string msg)
    {
        File.AppendAllText(
            "data/chat.txt",
            msg + "\n"
        );
    }
}
Ý nghĩa
users.json

Lưu user dạng:

{"username":"admin","password":"123"}
chat.txt
hello
hi
test
BƯỚC 6 — Program.cs

Đây là server chính.

Program.cs
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class Program
{
    static List<Socket> clients =
        new List<Socket>();

    static void Main()
    {
        IPEndPoint serverInfor =
            new IPEndPoint(IPAddress.Any, 8080);

        Socket serverListen =
            new Socket(
                AddressFamily.InterNetwork,
                SocketType.Stream,
                ProtocolType.Tcp
            );

        serverListen.Bind(serverInfor);

        serverListen.Listen(10);

        Console.WriteLine("Dang cho khach...");

        while (true)
        {
            Socket staff =
                serverListen.Accept();

            Thread t =
                new Thread(handleClient);

            t.Start(staff);
        }
    }

    static void handleClient(object obj)
    {
        Socket staff = (Socket)obj;

        byte[] bytes = new byte[4096];

        int bytesRec =
            staff.Receive(bytes);

        string requestData =
            Encoding.UTF8.GetString(
                bytes,
                0,
                bytesRec
            );

        Console.WriteLine(requestData);

        string requestLine =
            requestData.Split('\n')[0];

        // GET /
        if (requestLine.Contains("GET / "))
        {
            sendFile(
                staff,
                "pages/login.html"
            );
        }

        // GET /chat
        else if (requestLine.Contains("GET /chat"))
        {
            sendFile(
                staff,
                "pages/chat.html"
            );
        }

        // POST /login
        else if (requestLine.Contains("POST /login"))
        {
            string body =
                requestData.Split("\r\n\r\n")[1];

            User u = new User();

            string[] arr =
                body.Split('&');

            u.username =
                arr[0].Split('=')[1];

            u.password =
                arr[1].Split('=')[1];

            FileManager.saveUser(u);

            string response =
                "<html><body>Login OK</body></html>";

            sendHTML(staff, response);
        }

        staff.Close();
    }

    static void sendFile(
        Socket staff,
        string filename)
    {
        string html =
            File.ReadAllText(filename);

        sendHTML(staff, html);
    }

    static void sendHTML(
        Socket staff,
        string html)
    {
        string responseData =
            "HTTP/1.1 200 OK\r\n";

        responseData +=
            "Content-Type: text/html\r\n";

        responseData +=
            $"Content-Length: {html.Length}\r\n";

        responseData += "\r\n";

        responseData += html;

        byte[] msg =
            Encoding.UTF8.GetBytes(
                responseData
            );

        staff.Send(msg);
    }
}
Chạy project

Nhấn:

Ctrl + F5
Browser mở
http://localhost:8080
Kết quả

✅ login page hiện
✅ POST login hoạt động
✅ lưu users.json
✅ GET chat page được

Nhưng…
WebSocket chưa làm 😈

Hiện tại mới là HTTP.

Muốn WebSocket thật

Phải:

1. parse Upgrade header
2. websocket handshake
3. encode/decode frame
4. broadcast message

Cái này hardcore hơn nhiều 💀