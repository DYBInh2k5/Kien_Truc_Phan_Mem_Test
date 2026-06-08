using Microsoft.Data.Sqlite;
using System.IO;

var builder = WebApplication.CreateBuilder(args);

// Cấu hình cổng chạy 5001 cho SSO Service lắng nghe trên mọi card mạng (0.0.0.0)
// Điều này cực kỳ quan trọng để cho phép Container Docker bên ngoài (FastAPI) kết nối thành công.
builder.WebHost.UseUrls("http://0.0.0.0:5001");

var app = builder.Build();

/// <summary>
/// Hàm tự động tìm và phân giải đường dẫn tương đối của tệp database SQLite (orders.db).
/// Do dự án C# Microservice chạy trên Windows host và Python chạy trong Docker container có thư mục làm việc khác nhau,
/// hàm này duyệt ngược cây thư mục cha để tìm đúng vị trí file orders.db chung tại "src/web_mvc/orders.db".
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
        dbPath = "orders.db"; // Fallback về thư mục hiện tại nếu không tìm thấy
    }

    Console.WriteLine($"[SSO Service] Resolving SQLite database path to: {dbPath}");
    return $"Data Source={dbPath}";
}

// ==========================================
// ENDPOINT: ĐĂNG NHẬP SSO (Xác thực tài khoản thật)
// ==========================================
app.MapPost("/api/sso/login", (LoginRequest request) => {
    var connectionString = GetDatabaseConnectionString();
    
    // Sử dụng ADO.NET Microsoft.Data.Sqlite để kết nối SQLite
    using var connection = new SqliteConnection(connectionString);
    try
    {
        connection.Open();
        
        // Truy vấn bảng users bằng SQL Parameterization để chống SQL Injection
        var query = "SELECT id, username, email, is_admin FROM users WHERE username = @u AND password = @p";
        using var command = new SqliteCommand(query, connection);
        command.Parameters.AddWithValue("@u", request.Username);
        command.Parameters.AddWithValue("@p", request.Password);

        using var reader = command.ExecuteReader();
        if (reader.Read())
        {
            // Trích xuất dữ liệu từ Database
            var id = reader.GetInt32(0);
            var username = reader.GetString(1);
            var email = reader.GetString(2);
            var isAdmin = reader.GetInt32(3) == 1;

            // Sinh Token bảo mật giả lập dạng JWT
            string token = $"sso_token_secure_{username}_{Guid.NewGuid().ToString("N").Substring(0, 8)}";
            Console.WriteLine($"[SSO Service] User '{username}' authenticated successfully via SQLite.");
            
            // Trả về kết quả JSON chuẩn hóa
            return Results.Ok(new { 
                message = "SSO Dịch vụ C#: Đăng nhập thành công!", 
                token = token,
                user = new { username = username, email = email, is_admin = isAdmin }
            });
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[SSO Service Error] {ex.Message}");
        return Results.Json(new { error = $"SSO Dịch vụ C# lỗi hệ thống: {ex.Message}" }, statusCode: 500);
    }

    Console.WriteLine($"[SSO Service Warning] Failed login attempt for user: '{request.Username}'");
    return Results.BadRequest(new { error = "SSO Dịch vụ C#: Sai tài khoản hoặc mật khẩu!" });
});

// ==========================================
// ENDPOINT: XÁC MINH PHIÊN ĐĂNG NHẬP (Token Verification)
// ==========================================
app.MapGet("/api/sso/verify", (string token) => {
    if (token != null && token.StartsWith("sso_token_secure_"))
    {
        var parts = token.Split('_');
        var username = parts.Length > 3 ? parts[3] : "user";
        return Results.Ok(new { valid = true, user = username, source = "SSO C# Microservice" });
    }
    return Results.Json(new { valid = false, error = "SSO Dịch vụ C#: Token không hợp lệ!" }, statusCode: 401);
});

app.Run();

// DTO định nghĩa cấu trúc dữ liệu đầu vào nhận về từ FastAPI Web
public record LoginRequest(string Username, string Password);
