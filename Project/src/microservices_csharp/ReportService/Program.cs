using Microsoft.Data.Sqlite;
using System.IO;

var builder = WebApplication.CreateBuilder(args);

// Cấu hình cổng 5003 cho Report Service lắng nghe trên mọi card mạng (0.0.0.0)
// Cho phép FastAPI Web Component gửi yêu cầu HTTP Proxy lấy báo cáo động.
builder.WebHost.UseUrls("http://0.0.0.0:5003");

var app = builder.Build();

/// <summary>
/// Hàm phân giải đường dẫn cơ sở dữ liệu SQLite chung (orders.db).
/// </summary>
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

// ==========================================
// ENDPOINT: LẤY BÁO CÁO THỐNG KÊ DOANH THU ĐỘNG
// ==========================================
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
        
        // Truy vấn lấy ra chuỗi chi tiết (details) của toàn bộ đơn hàng trong database
        var query = "SELECT details FROM orders";
        using var command = new SqliteCommand(query, connection);
        using var reader = command.ExecuteReader();
        
        // Bắt đầu quét qua từng dòng đơn hàng
        while (reader.Read())
        {
            totalOrders++;
            var details = reader.GetString(0);
            
            // Phân tích loại đơn hàng: Chứa chuỗi "(Express)" hoặc "Express"
            bool isExpress = details.Contains("(Express)") || details.Contains("Express");
            double shippingCost = isExpress ? 15.0 : 2.5; // Phí ship tương ứng của từng loại đơn
            
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

            // Phân tích giá sản phẩm từ chuỗi chi tiết để tính tổng doanh thu động thực tế
            double productPrice = 0;
            if (details.Contains("Product ID: 1"))
            {
                productPrice = 2000.00; // MacBook Pro M3
            }
            else if (details.Contains("Product ID: 2"))
            {
                productPrice = 1200.00; // iPhone 15 Pro Max
            }
            else if (details.Contains("Product ID: 3"))
            {
                productPrice = 150.00;  // Leopold FC900
            }

            // Doanh thu của đơn hàng = Giá sản phẩm + Phí vận chuyển
            totalRevenue += (productPrice + shippingCost);
        }
        Console.WriteLine($"[Report Service] Generated statistics for {totalOrders} orders via SQLite database query.");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[Report Service Error] {ex.Message}");
        return Results.Json(new { error = $"C# Report Service lỗi hệ thống: {ex.Message}" }, statusCode: 500);
    }

    // Trả về kết quả thống kê tài chính chi tiết
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
