var builder = WebApplication.CreateBuilder(args);

// Cấu hình cổng chạy 5001 cho SSO Service
builder.WebHost.UseUrls("http://localhost:5001");

var app = builder.Build();

app.MapPost("/api/sso/login", (LoginRequest request) => {
    if (request.Username == "admin" && request.Password == "123")
    {
        return Results.Ok(new { 
            message = "SSO Dịch vụ C#: Đăng nhập thành công!", 
            token = "sso_token_secure_admin_xyz",
            user = new { username = "admin", email = "admin@sso.csharp" }
        });
    }
    return Results.BadRequest(new { error = "SSO Dịch vụ C#: Sai tài khoản hoặc mật khẩu!" });
});

app.MapGet("/api/sso/verify", (string token) => {
    if (token == "sso_token_secure_admin_xyz")
    {
        return Results.Ok(new { valid = true, user = "admin", source = "SSO C# Microservice" });
    }
    return Results.Json(new { valid = false, error = "SSO Dịch vụ C#: Token không hợp lệ!" }, statusCode: 401);
});

app.Run();

public record LoginRequest(string Username, string Password);
