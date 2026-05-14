using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace LAB06
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // 1. Khởi tạo IP + Port
            IPEndPoint serverInfor = new IPEndPoint(IPAddress.Any, 8080);

            // 2. Tạo TCP Socket
            Socket server = new Socket(
                AddressFamily.InterNetwork,
                SocketType.Stream,
                ProtocolType.Tcp);

            server.Bind(serverInfor);
            server.Listen(10);

            Console.WriteLine("Server dang chay tai http://localhost:8080");

            // 3. Nhận nhiều client (multi-thread)
            while (true)
            {
                Socket client = server.Accept();
                Console.WriteLine($"Client: {client.RemoteEndPoint}");

                Thread t = new Thread(HandleClient);
                t.Start(client);
            }
        }

        // 4. Xử lý từng client
        static void HandleClient(object obj)
        {
            Socket client = (Socket)obj;

            try
            {
                string requestData = "";
                byte[] buffer = new byte[1024];

                // 5. Nhận HTTP request
                while (true)
                {
                    int bytesRec = client.Receive(buffer);
                    if (bytesRec == 0) break;

                    requestData += Encoding.ASCII.GetString(buffer, 0, bytesRec);

                    // HTTP kết thúc bằng dòng trống
                    if (requestData.Contains("\r\n\r\n"))
                        break;
                }

                Console.WriteLine("==== REQUEST ====");
                Console.WriteLine(requestData);

                // 6. Lấy dòng đầu: GET /login HTTP/1.1
                string firstLine = requestData.Split('\n')[0];

                // Lấy path và method
                string method = "";
                string path = "/";
                
                string[] parts = firstLine.Split(' ');
                if (parts.Length > 1)
                {
                    method = parts[0];
                    path = parts[1];
                }

                Console.WriteLine("Method: " + method);
                Console.WriteLine("Path: " + path);

                // 7. Routing (điểm chính bài này)
                string responseBody = "";
                string responseStatus = "200 OK";

                string htmlTemplate = @"<!DOCTYPE html>
<html lang=""en"">
<head>
    <meta charset=""UTF-8"">
    <meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">
    <title>{0}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #f0f2f5; color: #333; }}
        .header {{ background-color: #0078d4; padding: 15px; text-align: center; }}
        .header a {{ color: white; text-decoration: none; margin: 0 15px; font-size: 18px; font-weight: bold; }}
        .header a:hover {{ text-decoration: underline; }}
        .container {{ max-width: 800px; margin: 40px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        h1 {{ color: #0078d4; }}
    </style>
</head>
<body>
    <div class=""header"">
        <a href=""/"">Home</a>
        <a href=""/login"">Login</a>
        <a href=""/about"">About</a>
        <a href=""/contact"">Contact</a>
    </div>
    <div class=""container"">
        <h1>{1}</h1>
        <p>{2}</p>
    </div>
</body>
</html>";

                if (method == "GET")
                {
                    switch (path)
                    {
                        case "/":
                            responseBody = string.Format(htmlTemplate, "Home", "Welcome to oTu Server", "Day la trang chu cua he thong. Vui long chon cac menu ben tren de dieu huong.");
                            break;

                        case "/login":
                            responseBody = string.Format(htmlTemplate, "Login", "Login Page", 
                                "Vui long nhap ten tai khoan va mat khau de dang nhap vao he thong.<br><br>" +
                                "<form><input type='text' placeholder='Username' style='padding:8px; margin-bottom:10px;'><br>" +
                                "<input type='password' placeholder='Password' style='padding:8px; margin-bottom:10px;'><br>" +
                                "<button type='button' style='padding:8px 15px; background-color:#0078d4; color:white; border:none; border-radius:4px;'>Login</button></form>");
                            break;

                        case "/contact":
                            responseBody = string.Format(htmlTemplate, "Contact", "Contact Us", 
                                "Email ho tro: <a href='mailto:support@otu.com'>support@otu.com</a><br>" +
                                "So dien thoai: <strong>0123 456 789</strong><br>" +
                                "Dia chi: 123 Duong ABC, Quan XYZ, TP.HCM");
                            break;

                        case "/about":
                            responseBody = string.Format(htmlTemplate, "About", "About Page", "He thong quan ly don hang oTu version 1.0.<br>Duoc phat trien de quan ly ban hang hieu qua hon va thuc hanh HTTP Server voi C#.");
                            break;

                        default:
                            responseStatus = "404 Not Found";
                            responseBody = string.Format(htmlTemplate, "404", "404 Not Found", "Rất tiếc, trang bạn tìm kiếm không tồn tại.");
                            break;
                    }
                }
                else
                {
                    responseStatus = "405 Method Not Allowed";
                    responseBody = string.Format(htmlTemplate, "405", "Method Not Allowed", $"Phuong thuc {method} khong duoc server ho tro. Chi ho tro GET.");
                }

                // 8. Tạo HTTP response
                int contentLength = Encoding.UTF8.GetByteCount(responseBody);

                string responseHeader =
                    $"HTTP/1.1 {responseStatus}\r\n" +
                    "Server: oTu\r\n" +
                    "Content-Type: text/html; charset=UTF-8\r\n" +
                    $"Content-Length: {contentLength}\r\n" +
                    "Connection: close\r\n" +
                    "\r\n";

                string fullResponse = responseHeader + responseBody;

                // 9. Gửi về client
                byte[] responseBytes = Encoding.UTF8.GetBytes(fullResponse);
                client.Send(responseBytes);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Loi: " + ex.Message);
            }
            finally
            {
                try { client.Shutdown(SocketShutdown.Both); } catch { }
                client.Close();
                Console.WriteLine("Client disconnected");
            }
        }
    }
}