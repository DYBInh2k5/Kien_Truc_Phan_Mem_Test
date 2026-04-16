using System;
using System.Net.Sockets;
using System.Text;

static class ClientApp
{
    public static void Start()
    {
        try
        {
            using Socket client = new Socket(AddressFamily.InterNetwork,
                                           SocketType.Stream,
                                           ProtocolType.Tcp);

            client.Connect("127.0.0.1", 8080);
            Console.WriteLine("Connected to server 127.0.0.1:8080");

            while (true)
            {
                Console.Write("Nhap command: ");
                string input = Console.ReadLine();
                if (string.IsNullOrWhiteSpace(input)) continue;
                if (input.Equals("exit", StringComparison.OrdinalIgnoreCase)) break;

                string msg = input + "<EOF>";
                client.Send(Encoding.ASCII.GetBytes(msg));

                byte[] buffer = new byte[1024];
                int bytes = client.Receive(buffer);
                string response = Encoding.ASCII.GetString(buffer, 0, bytes);
                Console.WriteLine("Server: " + response);
            }

            try { client.Shutdown(SocketShutdown.Both); } catch { }
        }
        catch (SocketException se)
        {
            Console.WriteLine("Socket error: " + se.Message);
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error: " + ex.Message);
        }
    }
}
