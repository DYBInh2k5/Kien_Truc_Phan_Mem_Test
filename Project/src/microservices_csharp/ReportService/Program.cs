var builder = WebApplication.CreateBuilder(args);

// Cấu hình cổng 5003 cho Report Service
builder.WebHost.UseUrls("http://localhost:5003");

var app = builder.Build();

app.MapGet("/api/report/summary", () => {
    // Giả lập dữ liệu thống kê từ database
    return Results.Ok(new {
        total_orders = 52,
        total_revenue = 12450.50,
        shipping_summary = new[] {
            new { type = "Standard", count = 38, cost = 95.0 },
            new { type = "Express", count = 14, cost = 210.0 }
        },
        system = "C# Statistical Report Microservice",
        generated_at = DateTime.Now
    });
});

app.Run();
