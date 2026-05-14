using System.Net.Sockets;
using System.Net;
using System.Text;

namespace _8._12_test
{
    internal class Program
    {
        /// <summary>
        /// Khởi tạo Server Socket lắng nghe kết nối TCP tại port 8080.
        /// Sử dụng mô hình Multi-threading: mỗi Client kết nối sẽ được xử lý trong 1 Thread riêng biệt.
        /// </summary>
        static void Main(string[] args)
        {
            IPEndPoint serverInfo = new IPEndPoint(IPAddress.Any, 8080);
            Socket serverListen = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            serverListen.Bind(serverInfo);
            serverListen.Listen(10);

            Console.WriteLine("Server started on http://localhost:8080");

            while (true)
            {
                Socket staff = serverListen.Accept();
                Thread t = new Thread(() => HandleClient(staff));
                t.Start();
            }
        }

        /// <summary>
        /// Tiếp nhận và xử lý dữ liệu từ Client (Browser).
        /// Thực hiện: Nhận Byte -> Decode UTF8 -> Parse HTTP Request (Method, Path, Cookie, Body).
        /// Sau đó chuyển tiếp sang lớp Router để xử lý logic.
        /// </summary>
        static void HandleClient(Socket staff)
        {
            try
            {
                byte[] bytes = new byte[10240];
                int bytesRec = staff.Receive(bytes);
                if (bytesRec <= 0) return;

                string requestData = Encoding.UTF8.GetString(bytes, 0, bytesRec);
                string[] parts = requestData.Split("\r\n\r\n");
                
                string headers = parts[0];
                string body = parts.Length > 1 ? parts[1] : "";

                string[] headerLines = headers.Split("\r\n");
                if (headerLines.Length == 0) return;

                string[] firstLine = headerLines[0].Split(' ');
                if (firstLine.Length < 2) return;

                string method = firstLine[0];
                string path = firstLine[1];

                string cookie = "";
                foreach (var line in headerLines)
                {
                    if (line.StartsWith("Cookie:"))
                    {
                        cookie = line.Substring(7).Trim();
                    }
                }

                Router.Handle(staff, method, path, body, cookie);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                staff.Close();
            }
        }
    }
}
