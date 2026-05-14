using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using SATestSocket.Patterns;
using SATestSocket.Models;

namespace _8._13_test
{
    /// <summary>
    /// Lớp chính điều khiển toàn bộ web server chạy trên giao thức Socket TCP.
    /// </summary>
    internal class Program
    {
        // Danh sách phòng chat toàn cục
        static List<ChatRoom> chatRooms = new List<ChatRoom>
        {
            new ChatRoom { id = 1, lastActivity = DateTime.MinValue },
            new ChatRoom { id = 2, lastActivity = DateTime.MinValue }
        };

        static void Main(string[] args)
        {
            // Thiết lập địa chỉ IP (tất cả các card mạng) và cổng 8080 cho server
            IPEndPoint serverInfor =
                new IPEndPoint(IPAddress.Any, 8080);

            // Tạo Socket chuẩn TCP/IP
            Socket serverListen = new Socket(
                AddressFamily.InterNetwork,
                SocketType.Stream,
                ProtocolType.Tcp);

            // Gắn Socket vào địa chỉ và cổng đã chọn
            serverListen.Bind(serverInfor);

            // Bắt đầu lắng nghe kết nối (hàng đợi tối đa 10 kết nối)
            serverListen.Listen(10);

            Console.WriteLine("Server dang chay tai http://localhost:8080");
            Console.WriteLine("Dang cho khach...");

            // Vòng lặp vô tận để server luôn trực chiến chấp nhận khách hàng mới
            while (true)
            {
                // Chấp nhận một kết nối mới từ trình duyệt
                Socket staff = serverListen.Accept();

                // Tạo một luồng (Thread) mới cho mỗi khách hàng để không gây tắc nghẽn (Đa luồng)
                Thread t = new Thread(handleClient);

                t.Start(staff);
            }
        }

        /// <summary>
        /// Hàm xử lý từng yêu cầu (Request) từ trình duyệt của khách hàng.
        /// </summary>
        static void handleClient(object? obj)
        {
            if (obj == null) return;
            Socket staff = (Socket)obj;

            try
            {
                string requestData = "";
                byte[] buffer = new byte[4096];
                int bytesRec = staff.Receive(buffer);
                requestData = Encoding.UTF8.GetString(buffer, 0, bytesRec);

                if (string.IsNullOrEmpty(requestData)) return;

                Console.WriteLine("\n--- NEW REQUEST ---");
                Console.WriteLine(requestData);

                string[] requestLines = requestData.Split(new[] { "\r\n", "\n" }, StringSplitOptions.None);
                string firstLine = requestLines[0];
                string[] firstLineParts = firstLine.Split(' ');
                
                if (firstLineParts.Length < 2) return;
                
                string method = firstLineParts[0];
                string url = firstLineParts[1];

                string body = "";
                string contentType = "text/html; charset=utf-8";

                // ROUTING
                // 1. GET / - Trang chủ
                if (method == "GET" && url == "/")
                {
                    body = @"<html><body>
                        <h1>Student Information</h1>
                        <p>ID: 23000001</p>
                        <p>Fullname: Nguyen Van A</p>
                        <p>PC Number: PC-01</p>
                        <hr/>
                        <a href='/login'>Login to Chat Room</a>
                    </body></html>";
                }
                // 2. GET /login - Trang đăng nhập
                else if (method == "GET" && url == "/login")
                {
                    body = @"<html><body>
                        <h1>Login</h1>
                        <form method='POST' action='/login'>
                            Username: <input name='username' required/><br/>
                            Password: <input type='password' name='password' required/><br/>
                            <button type='submit'>Login</button>
                        </form>
                    </body></html>";
                }
                // 3. POST /login - Xử lý đăng nhập
                else if (method == "POST" && url == "/login")
                {
                    string reqBody = requestLines.Last();
                    var data = ParseFormUrlEncoded(reqBody);
                    string user = data.ContainsKey("username") ? data["username"] : "";
                    string pass = data.ContainsKey("password") ? data["password"] : "";

                    // Tìm đường dẫn file users.json một cách an toàn
                    string jsonPath = "";
                    string currentDir = AppDomain.CurrentDomain.BaseDirectory;
                    
                    // Danh sách ưu tiên tìm kiếm file
                    List<string> possiblePaths = new List<string> {
                        Path.Combine(currentDir, "Data", "users.json"),
                        Path.Combine(Directory.GetCurrentDirectory(), "8.13_test", "Data", "users.json"),
                        Path.Combine(Directory.GetCurrentDirectory(), "Data", "users.json"),
                        "8.13_test/Data/users.json",
                        "Data/users.json"
                    };

                    foreach (var path in possiblePaths)
                    {
                        if (File.Exists(path))
                        {
                            jsonPath = path;
                            break;
                        }
                    }

                    // Nếu vẫn không thấy, quét toàn bộ thư mục gốc của giải pháp
                    if (string.IsNullOrEmpty(jsonPath))
                    {
                        var rootDir = new DirectoryInfo(Directory.GetCurrentDirectory());
                        // Lùi lại tối đa 3 cấp thư mục để tìm (trường hợp chạy từ bin/Debug/net8.0)
                        for (int i = 0; i < 4; i++)
                        {
                            var files = rootDir.GetFiles("users.json", SearchOption.AllDirectories);
                            if (files.Length > 0)
                            {
                                jsonPath = files[0].FullName;
                                break;
                            }
                            if (rootDir.Parent == null) break;
                            rootDir = rootDir.Parent;
                        }
                    }

                    if (string.IsNullOrEmpty(jsonPath))
                    {
                         Console.WriteLine("CRITICAL ERROR: users.json NOT FOUND in any searched locations.");
                         body = "<html><body><h1>System Error</h1><p>Database file (users.json) not found.</p></body></html>";
                    }
                    else
                    {
                        var usersJson = File.ReadAllText(jsonPath);
                        var users = JsonSerializer.Deserialize<List<User>>(usersJson);

                        bool isValid = users.Any(u => u.username == user && u.password == pass);

                        if (isValid)
                        {
                            // Redirect sang /chat
                            byte[] redirect = Encoding.UTF8.GetBytes("HTTP/1.1 302 Found\r\nLocation: /chat\r\n\r\n");
                            staff.Send(redirect);
                            return;
                        }
                        else
                        {
                            body = "<html><body><h1>Login Failed</h1><p>Invalid username or password.</p><a href='/login'>Try again</a></body></html>";
                        }
                    }
                }
                // 4. GET /chat - Danh sách chat rooms
                else if (method == "GET" && url == "/chat")
                {
                    body = "<html><body><h1>Chat Rooms</h1><ul>";
                    foreach (var room in chatRooms)
                    {
                        bool isOnline = (DateTime.Now - room.lastActivity).TotalMinutes < 3;
                        if (!isOnline) room.messages.Clear();

                        string status = isOnline ? "<span style='color:green'>(Online)</span>" : "<span style='color:gray'>(Offline)</span>";
                        body += $"<li>Room {room.id}: {status} - <a href='/chat/{room.id}'>Join</a></li>";
                    }
                    body += "</ul></body></html>";
                }
                // 5. GET /chat/:id - Chi tiết phòng chat
                else if (method == "GET" && url.StartsWith("/chat/"))
                {
                    int roomId = int.Parse(url.Replace("/chat/", ""));
                    var room = chatRooms.FirstOrDefault(r => r.id == roomId);

                    if (room != null)
                    {
                        body = $"<html><body><h1>Room {roomId}</h1><div style='border:1px solid #ccc; height:300px; overflow-y:scroll; padding:10px;'>";
                        foreach (var m in room.messages)
                        {
                            body += $"<p>[{m.time:HH:mm:ss}] <b>{m.username}</b>: {m.content}</p>";
                        }
                        body += "</div><hr/>";
                        body += $@"<form method='POST' action='/chat/{roomId}'>
                            Name: <input name='username' required/><br/>
                            Message: <input name='message' style='width:300px' required/>
                            <button type='submit'>Send</button>
                        </form>
                        <br/><a href='/chat'>Back to rooms</a>
                        </body></html>";
                    }
                    else { body = "Room not found"; }
                }
                // 6. POST /chat/:id - Gửi tin nhắn
                else if (method == "POST" && url.StartsWith("/chat/"))
                {
                    int roomId = int.Parse(url.Replace("/chat/", ""));
                    var room = chatRooms.FirstOrDefault(r => r.id == roomId);

                    if (room != null)
                    {
                        string reqBody = requestLines.Last();
                        var data = ParseFormUrlEncoded(reqBody);
                        
                        room.messages.Add(new Message { 
                            username = data["username"], 
                            content = data["message"], 
                            time = DateTime.Now 
                        });
                        room.lastActivity = DateTime.Now;

                        // Redirect back to chat room
                        byte[] redirect = Encoding.UTF8.GetBytes($"HTTP/1.1 302 Found\r\nLocation: /chat/{roomId}\r\n\r\n");
                        staff.Send(redirect);
                        return;
                    }
                }
                else
                {
                    body = "<html><body><h1>404 Not Found</h1></body></html>";
                }

                byte[] msg = ServerFacade.buildResponse(body);
                staff.Send(msg);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }
            finally
            {
                staff.Shutdown(SocketShutdown.Both);
                staff.Close();
            }
        }

        // Helper để parse form data
        static Dictionary<string, string> ParseFormUrlEncoded(string body)
        {
            var result = new Dictionary<string, string>();
            var pairs = body.Split('&');
            foreach (var pair in pairs)
            {
                var parts = pair.Split('=');
                if (parts.Length == 2)
                    result[WebUtility.UrlDecode(parts[0])] = WebUtility.UrlDecode(parts[1]);
            }
            return result;
        }
    }
}
