using System.Text.Json;

internal class FileManager
{
    public static void saveUser(User user)
    {
        string json = JsonSerializer.Serialize(user);
        File.AppendAllText("data/users.json", json + "\n");
    }

    public static void saveChat(string msg)
    {
        File.AppendAllText("data/chat.txt", msg + "\n");
    }
}