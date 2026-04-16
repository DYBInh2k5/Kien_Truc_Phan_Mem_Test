using System;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length > 0 && args[0].Equals("server", StringComparison.OrdinalIgnoreCase))
        {
            ServerApp.Start();
            return;
        }

        if (args.Length > 0 && args[0].Equals("client", StringComparison.OrdinalIgnoreCase))
        {
            ClientApp.Start();
            return;
        }

        Console.WriteLine("Usage: dotnet run -- server|client");
        Console.WriteLine("Starting server by default...\n");
        ServerApp.Start();
    }
}
