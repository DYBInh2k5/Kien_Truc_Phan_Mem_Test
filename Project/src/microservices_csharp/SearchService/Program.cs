var builder = WebApplication.CreateBuilder(args);

// Cấu hình cổng 5002 cho Search Service
builder.WebHost.UseUrls("http://localhost:5002");

var app = builder.Build();

app.MapGet("/api/search/orders/{id:int}", (int id) => {
    // Giả lập tìm kiếm dữ liệu nâng cao
    if (id == 101)
    {
        return Results.Ok(new {
            id = 101,
            details = "Laptop XYZ (Bản nâng cấp C# Search)",
            status = "Shipped",
            tracking_code = "TRACK_999",
            searched_at = DateTime.Now
        });
    }
    else if (id == 102)
    {
        return Results.Ok(new {
            id = 102,
            details = "Bàn Phím Cơ (Bản nâng cấp C# Search)",
            status = "Pending",
            tracking_code = "TRACK_333",
            searched_at = DateTime.Now
        });
    }
    return Results.Json(new { error = $"Không tìm thấy đơn hàng {id} trong C# Search Microservice!" }, statusCode: 404);
});

app.Run();
