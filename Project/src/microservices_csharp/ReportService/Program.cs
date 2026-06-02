var builder = WebApplication.CreateBuilder(args);

// Cấu hình cổng 5003 cho Report Service
builder.WebHost.UseUrls("http://localhost:5003");

var app = builder.Build();

app.MapGet("/api/report/summary", () => {
    // Giả lập dữ liệu thống kê từ database
    return Results.Ok(new {
        total_orders = 152,
        total_revenue = 35420.00,
        shipping_summary = new[] {
            new { type = "Standard", count = 112, cost = 280.0 },
            new { type = "Express", count = 40, cost = 600.0 }
        },
        system = "C# Statistical Report Microservice",
        generated_at = DateTime.Now
    });
});

app.Run();
