# run_microservices.ps1
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   Kích Hoạt Cụm C# Microservices (.NET 8.0)  " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Di chuyển đến thư mục chứa script này
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptPath

# 1. Chạy SSOService (Cổng 5001)
Write-Host "Khởi chạy SSOService (Cổng 5001) trong cửa sổ mới..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k dotnet run --project SSOService" -WorkingDirectory $ScriptPath

# 2. Chạy SearchService (Cổng 5002)
Write-Host "Khởi chạy SearchService (Cổng 5002) trong cửa sổ mới..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k dotnet run --project SearchService" -WorkingDirectory $ScriptPath

# 3. Chạy ReportService (Cổng 5003)
Write-Host "Khởi chạy ReportService (Cổng 5003) trong cửa sổ mới..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k dotnet run --project ReportService" -WorkingDirectory $ScriptPath

Write-Host "`n[Thành Công] Đã khởi chạy cả 3 C# Microservices!" -ForegroundColor Green
Write-Host "Vui lòng kiểm tra các cửa sổ Console mới mở để xem Log." -ForegroundColor Gray
Write-Host "Tắt các cửa sổ Console đó để tắt hẳn các Microservices khi kết thúc." -ForegroundColor Gray
