using Microsoft.Data.Sqlite;
using System.IO;

var builder = WebApplication.CreateBuilder(args);

// Cấu hình cổng 5003 cho Report Service
builder.WebHost.UseUrls("http://localhost:5003");

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

    Console.WriteLine($"[Report Service] Resolving SQLite database path to: {dbPath}");
    return $"Data Source={dbPath}";
}

app.MapGet("/api/report/summary", () => {
    var connectionString = GetDatabaseConnectionString();
    int totalOrders = 0;
    double totalRevenue = 0;
    int standardCount = 0;
    int expressCount = 0;
    double standardCostSum = 0;
    double expressCostSum = 0;

    using var connection = new SqliteConnection(connectionString);
    try
    {
        connection.Open();
        var query = "SELECT details FROM orders";
        using var command = new SqliteCommand(query, connection);
        using var reader = command.ExecuteReader();
        while (reader.Read())
        {
            totalOrders++;
            var details = reader.GetString(0);
            
            bool isExpress = details.Contains("(Express)") || details.Contains("Express");
            double shippingCost = isExpress ? 15.0 : 2.5;
            
            if (isExpress)
            {
                expressCount++;
                expressCostSum += shippingCost;
            }
            else
            {
                standardCount++;
                standardCostSum += shippingCost;
            }

            double productPrice = 0;
            if (details.Contains("Product ID: 1"))
            {
                productPrice = 2000.00;
            }
            else if (details.Contains("Product ID: 2"))
            {
                productPrice = 1200.00;
            }
            else if (details.Contains("Product ID: 3"))
            {
                productPrice = 150.00;
            }

            totalRevenue += (productPrice + shippingCost);
        }
        Console.WriteLine($"[Report Service] Generated statistics for {totalOrders} orders via SQLite database query.");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[Report Service Error] {ex.Message}");
        return Results.Json(new { error = $"C# Report Service lỗi hệ thống: {ex.Message}" }, statusCode: 500);
    }

    return Results.Ok(new {
        total_orders = totalOrders,
        total_revenue = totalRevenue,
        shipping_summary = new[] {
            new { type = "Standard", count = standardCount, cost = standardCostSum },
            new { type = "Express", count = expressCount, cost = expressCostSum }
        },
        system = "C# Statistical Report Microservice (Real-time SQLite)",
        generated_at = DateTime.Now
    });
});

app.Run();
