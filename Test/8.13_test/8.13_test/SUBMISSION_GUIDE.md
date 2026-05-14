H??NG D?N N?P BÀI & K?CH B?N TR? L?I (Demo + Oral)

M?c ?ích: Tài li?u này giúp b?n chu?n b? màn hình ch?y ?ng d?ng và code khi n?p bài ki?m th?, ??ng th?i cung c?p các g?i ý tr? l?i cho bu?i ?ánh giá mi?ng.

1) YÊU C?U N?P BÀI (b?t bu?c)
- Folder `Results-screenshots` — ch?a 3–5 ?nh ch?p màn hình (Home, Login, Login success, Chat room, Console server).
- Folder `Code-DesignPatterns` — ch?a ?nh/ghi chú ph?n code áp d?ng design patterns (ví d? file `UserFactory.cs`, `ServerFacade.cs`).
- Folder `ProjectCode` — ch?a toàn b? mã ngu?n, th? m?c `HTML/`, `Models/`, `Patterns/`, `Data/` (??m b?o có `users.json`).

L?u ý tên file ?nh rõ ràng: `01_home.png`, `02_login.png`, `03_login_success.png`, `04_chat_room.png`, `05_console.png`.

2) KI?M TRA ?NG D?NG TR??C KHI N?P
- Ch?y: `dotnet run --project 8.13_test/8.13_test.csproj` ho?c ch?y t? Visual Studio.
- M?: `http://localhost:8080`.
- Ki?m tra: GET `/`, GET `/login`, POST `/login` (dùng tài kho?n trong `Data/users.json`), GET `/chat`, GET `/chat/1`, POST `/chat/1`.

3) M? MÀN HÌNH DEMO (g?i ý b? trí)
- Bên trái: c?a s? code (`Program.cs`, `Patterns/ServerFacade.cs`, `Patterns/UserFactory.cs`).
- Bên ph?i: trình duy?t hi?n th? trang web (http://localhost:8080).
- D??i cùng ho?c c?a s? riêng: console server showing request logs.

4) K?CH B?N TR? L?I (m?i ph?n nói ng?n, t?p trung)
- Gi?i thi?u nhanh: m?c tiêu bài (Raw Socket HTTP server, ko dùng ASP.NET), các công ngh? dùng (`C#`, `Socket`, `Thread`, `HTTP raw`).
- Gi?i thích lu?ng x? lý:
  - Server l?ng nghe c?ng 8080, `Accept()` k?t n?i, m?i client t?o 1 `Thread` và g?i `handleClient()`.
  - Trong `handleClient`: ??c request thô (Receive), parse dòng ??u ?? l?y `METHOD` và `URL`, ??c body (form) và parse `application/x-www-form-urlencoded`.
  - Tr? v? response b?ng `ServerFacade.buildResponse()` (Facade pattern) ho?c g?i redirect 302 khi c?n.
- Nêu rõ design patterns:
  - `UserFactory`: nhi?m v? t?o `User` (Factory Pattern).
  - `ServerFacade`: ?óng gói xây d?ng HTTP response (Facade Pattern).
- Demo tình hu?ng:
  - Th?c hi?n login v?i `nntu` / `56789`, cho gi?ng viên th?y console log request và redirect sang `/chat`.
  - Vào `/chat/1`, g?i tin nh?n, cho th?y room ???c ?ánh là online và l?ch s? xu?t hi?n.
  - Mô t? logic online/offline: n?u `lastActivity` cách > 3 phút thì phòng offline và `messages.Clear()`.

5) CÁC CÂU H?I GI? ??NH & G?I Ý TR? L?I NG?N
- "Làm th? nào server x? lý nhi?u client?" ? Multi-thread: t?o `Thread`/yêu c?u m?i k?t n?i.
- "Làm sao parse POST form?" ? l?y body string, g?i `ParseFormUrlEncoded()` ?? tách `key=value`.
- "Vì sao dùng Facade/Factory?" ? tách r?i trách nhi?m: xây d?ng response và t?o ??i t??ng.
- "N?u file `users.json` không tìm th?y?" ? ch? v? trí `Data/users.json`; trong code có logic tìm/scan nhi?u ???ng d?n; ki?m tra file có trong `ProjectCode/Data`.

6) L?U Ý V? ??O ??C & B?N QUY?N
- Không n?p code sao chép t? sinh viên khác.
- N?u dùng mã tham kh?o, ph?i hi?u và ch?nh s?a rõ.

7) KHI B? YÊU C?U S?A/DEBUG TRONG BU?I N?P
- Gi? bình t?nh, m? `Program.cs` và console logs.
- Gi?i thích b??c b?n s? làm (ví d?: ki?m tra `users.json` path, in request raw, parse body).

8) CHECKLIST TR??C KHI N?P
- Có 3 folder b?t bu?c ?úng tên.
- `users.json` n?m trong `ProjectCode/Data/`.
- Ch?y ???c `dotnet run` và truy c?p `localhost:8080`.
- 3–5 ?nh screenshot ?ã ??t tên h?p lý.

K?t thúc: dùng tài li?u này làm k?ch b?n demo ng?n (3–5 phút). Chu?n b? tr? l?i các câu h?i k? thu?t c? b?n v? Socket, Threading, HTTP parsing và design patterns.
