using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

static class ServerApp
{
    private static int orderId = 1;

    public static void Start()
    {
        IPEndPoint ip = new IPEndPoint(IPAddress.Any, 8080);
        Socket server = new Socket(AddressFamily.InterNetwork,
                                   SocketType.Stream,
                                   ProtocolType.Tcp);

        server.Bind(ip);
        server.Listen(10);

        Console.WriteLine("Server dang cho client...");

        while (true)
        {
            Socket client = server.Accept();
            Console.WriteLine($"Client connected: {client.RemoteEndPoint}");

            Thread t = new Thread(() => HandleClient(client));
            t.IsBackground = true;
            t.Start();
        }
    }

    static void HandleClient(Socket client)
    {
        string data = "";
        byte[] buffer = new byte[1024];

        try
        {
            while (true)
            {
                int bytesRec = client.Receive(buffer);
                if (bytesRec == 0) break;

                data += Encoding.ASCII.GetString(buffer, 0, bytesRec);

                if (data.Contains("<EOF>"))
                {
                    string command = data.Replace("<EOF>", "");
                    string response = ProcessCommand(command);
                    client.Send(Encoding.ASCII.GetBytes(response + "<EOF>"));
                    data = "";
                }
            }
        }
        catch (SocketException se)
        {
            Console.WriteLine("Socket error: " + se.Message);
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error: " + ex.Message);
        }

        Console.WriteLine("Client disconnected");
        try { client.Shutdown(SocketShutdown.Both); } catch { }
        client.Close();
    }

    static string ProcessCommand(string command)
    {
        Console.WriteLine("Nhan: " + command);

        string[] parts = command.Split('|', StringSplitOptions.RemoveEmptyEntries);
        if (parts.Length == 0) return "UNKNOWN_COMMAND";

        switch (parts[0])
        {
            case "CREATE_ORDER":
                return CreateOrder(parts);

            case "PING":
                return "PONG";

            case "LIST_ORDERS":
                return "NOT_IMPLEMENTED";

            default:
                return "UNKNOWN_COMMAND";
        }
    }

    static string CreateOrder(string[] parts)
    {
        if (parts.Length < 3) return "ERROR|INVALID_CREATE_ORDER";

        string user = parts[1];
        string products = parts[2];

        int id = Interlocked.Increment(ref orderId);
        Console.WriteLine($"Order {id} created for {user} | products={products}");

        return $"ORDER_CREATED|ID={id}";
    }
}
