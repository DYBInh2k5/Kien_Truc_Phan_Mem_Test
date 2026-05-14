using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace Readme_test
{
    class Program
    {
        static List<Socket> clients = new List<Socket>();

        static void Main()
        {
            IPEndPoint serverInfor = new IPEndPoint(IPAddress.Any, 8080);

            Socket serverListen = new Socket(
                AddressFamily.InterNetwork,
                SocketType.Stream,
                ProtocolType.Tcp
            );

            serverListen.Bind(serverInfor);
            serverListen.Listen(10);

            Console.WriteLine("Dang cho khach tai port 8080...");

            while (true)
            {
                Socket staff = serverListen.Accept();
                Thread t = new Thread(handleClient);
                t.Start(staff);
            }
        }

        static void handleClient(object? obj)
        {
            if (obj == null) return;
            Socket staff = (Socket)obj;

            try
            {
                byte[] bytes = new byte[4096];
                int bytesRec = staff.Receive(bytes);
                if (bytesRec == 0) return;

                string requestData = Encoding.UTF8.GetString(bytes, 0, bytesRec);
                Console.WriteLine(requestData);

                string requestLine = requestData.Split('\n')[0];

                // GET /
                if (requestLine.Contains("GET / ") || requestLine.Contains("GET /login"))
                {
                    sendFile(staff, "pages/login.html");
                }
                // GET /chat
                else if (requestLine.Contains("GET /chat"))
                {
                    sendFile(staff, "pages/chat.html");
                }
                // POST /login
                else if (requestLine.Contains("POST /login"))
                {
                    string[] parts = requestData.Split("\r\n\r\n");
                    if (parts.Length > 1)
                    {
                        string body = parts[1];
                        User u = new User();
                        string[] arr = body.Split('&');
                        if (arr.Length >= 2)
                        {
                            u.username = arr[0].Split('=')[1];
                            u.password = arr[1].Split('=')[1];

                            FileManager.saveUser(u);

                            string response = "<html><body>Login OK. <a href='/chat'>Go to Chat</a></body></html>";
                            sendHTML(staff, response);
                        }
                    }
                }
                else
                {
                    string response = "HTTP/1.1 404 Not Found\r\n\r\n";
                    staff.Send(Encoding.UTF8.GetBytes(response));
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }
            finally
            {
                staff.Close();
            }
        }

        static void sendFile(Socket staff, string filename)
        {
            if (File.Exists(filename))
            {
                string html = File.ReadAllText(filename);
                sendHTML(staff, html);
            }
            else
            {
                string response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found.";
                staff.Send(Encoding.UTF8.GetBytes(response));
            }
        }

        static void sendHTML(Socket staff, string html)
        {
            string responseData = "HTTP/1.1 200 OK\r\n";
            responseData += "Content-Type: text/html\r\n";
            responseData += $"Content-Length: {Encoding.UTF8.GetByteCount(html)}\r\n";
            responseData += "\r\n";
            responseData += html;

            byte[] msg = Encoding.UTF8.GetBytes(responseData);
            staff.Send(msg);
        }
    }
}
