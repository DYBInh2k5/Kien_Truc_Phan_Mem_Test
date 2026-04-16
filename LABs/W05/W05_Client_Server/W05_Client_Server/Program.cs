using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

// IP + Port 
IPEndPoint serverInfor = new IPEndPoint(IPAddress.Any, 8080);

// Protocol
Socket serverListen = new Socket(AddressFamily.InterNetwork
    , SocketType.Stream
    , ProtocolType.Tcp);

serverListen.Bind(serverInfor);

serverListen.Listen(10);

Console.WriteLine("Dang cho khach ... !");

Socket staff = serverListen.Accept();

Console.WriteLine($"... da nhan khach {staff.RemoteEndPoint.ToString()}");

string data = null;
byte[] bytes = null;

while (true)
{
    bytes = new byte[1024];
    int bytesRec = staff.Receive(bytes);

    data += Encoding.ASCII.GetString(bytes, 0, bytesRec);
    if (data.IndexOf("<EOF>"
        //"ketthuc"
        ) > -1)
    {
        break;
    }
    Console.WriteLine("... {0}", data);
}

Console.WriteLine("Khach noi : {0}", data);

byte[] msg = Encoding.ASCII.GetBytes(data);
staff.Send(msg);

staff.Shutdown(SocketShutdown.Both);

staff.Close();