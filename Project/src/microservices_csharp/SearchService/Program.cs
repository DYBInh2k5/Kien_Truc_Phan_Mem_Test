using Microsoft.Data.Sqlite;
using System.IO;

var builder = WebApplication.CreateBuilder(args);

// Cấu hình cổng 5002 cho Search Service
builder.WebHost.UseUrls("http://localhost:5002");

var app = builder.Build();

string GetDatabaseConnectionString()
{
    string currentDir = Directory.GetCurrentDirectory();
    string dbPath = "";
    while (currentDir != null)
    {
        string path1 = Path.Combine(currentDir, "Project", "src", "web_mvc", "orders.db");
        if (File.Exists(path1)) { dbPath = path1; break; }

        string path2 = Path.Combine(currentDir, "..", "web_mvc", "orders.db");
        if (File.Exists(path2)) { dbPath = Path.GetFullPath(path2); break; }

        string path3 = Path.Combine(currentDir, "..", "..", "web_mvc", "orders.db");
        if (File.Exists(path3)) { dbPath = Path.GetFullPath(path3); break; }

        string path4 = Path.Combine(currentDir, "web_mvc", "orders.db");
        if (File.Exists(path4)) { dbPath = path4; break; }

        currentDir = Directory.GetParent(currentDir)?.FullName;
    }

    if (string.IsNullOrEmpty(dbPath))
    {
        dbPath = "orders.db";
    }

    Console.WriteLine($"[Search Service] Resolving SQLite database path to: {dbPath}");
    return $"Data Source={dbPath}";
}

app.MapGet("/api/search/orders/{id:int}", (int id) => {
    var connectionString = GetDatabaseConnectionString();
    using var connection = new SqliteConnection(connectionString);
    try
    {
        connection.Open();
        var query = "SELECT id, details, status, tracking_code FROM orders WHERE id = @id";
        using var command = new SqliteCommand(query, connection);
        command.Parameters.AddWithValue("@id", id);

        using var reader = command.ExecuteReader();
        if (reader.Read())
        {
            var orderId = reader.GetInt32(0);
            var details = reader.GetString(1);
            var status = reader.GetString(2);
            var trackingCode = reader.GetString(3);

            Console.WriteLine($"[Search Service] Order ID {id} found in SQLite.");
            return Results.Ok(new {
                id = orderId,
                details = details + " (Đã xác minh qua C# Search)",
                status = status,
                tracking_code = trackingCode,
                searched_at = DateTime.Now
            });
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[Search Service Error] {ex.Message}");
        return Results.Json(new { error = $"C# Search Service lỗi hệ thống: {ex.Message}" }, statusCode: 500);
    }

    Console.WriteLine($"[Search Service Warning] Order ID {id} not found in database.");
    return Results.Json(new { error = $"Không tìm thấy đơn hàng {id} trong C# Search Microservice!" }, statusCode: 404);
});

app.Run();
