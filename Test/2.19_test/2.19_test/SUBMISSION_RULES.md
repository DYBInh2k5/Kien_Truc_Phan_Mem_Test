Rules for Submission — TEST (H??ng d?n n?p bài và cách trình bày khi ki?m tra)

1. Attendance Requirement (Yêu c?u có m?t)

- Ph?i có m?t tr?c ti?p t?i phòng Lab/gi? ki?m tra khi n?p và ch?m. N?u v?ng m?t không có phép, có th? không ???c ch?m.

2. Submission on the System (C?u trúc n?p bài)

- B?t bu?c n?p ??y ?? 3 ph?n trong m?t ZIP ho?c upload theo c?u trúc:
  - Part 1 ? Folder `Results-screenshots` (?nh ch?p giao di?n)
  - Part 2 ? Folder `Code-DesignPatterns` (?nh ch?p ?o?n code th? hi?n design pattern)
  - Part 3 ? Folder `ProjectCode` (toàn b? mã ngu?n d? án)
- N?u thi?u folder ho?c c?u trúc sai, ?i?m s? b? tr?.

3. Evidence and Screenshot Files (?nh ch?p, tên file)

- ??t tên file rõ ràng và theo quy ??c ?? gi?ng viên d? ki?m tra. Ví d?:
  - `01_Homepage.png`
  - `02_LoginPage.png`
  - `03_LoginSuccess_ChatList.png`
  - `04_ChatRoom_Online.png`
  - `05_ChatRoom_Offline.png`
  - `DP_Singleton.png` (ch? có `JsonService.getInstance()`)
  - `DP_Builder.png` (ch? có `RouteBuilder` và g?i trong `Program.cs`)
- ?nh c?n hi?n th? rõ n?i dung (URL thanh trình duy?t, form, cookie header khi có th?).

4. Application Functionality (Ch?y ???c ?ng d?ng)

- ?ng d?ng ph?i ch?y ???c. N?u không ch?y ho?c không th? demo, ?i?m b? tr? nghiêm tr?ng.
- Ki?m tra tr??c: t? th? m?c project ch?y `dotnet run`, m? http://localhost:8080.
- Ki?m tra tài kho?n: dùng `nntu` / `56789`.

5. Oral Explanation and Evaluation (Cách tr? l?i khi thuy?t trình)

- Khi gi?ng viên h?i, m? 2 màn hình chính ??ng th?i: "màn hình ch?y (browser)" và "màn hình code (IDE)".

- Trình t? demo (ng?n g?n, rõ ràng):
  1. M? `Program.cs` và gi?i thích flow chính: Socket l?ng nghe ? Accept ? Thread ? Parse HTTP ? Dispatch route.
  2. Trên browser: truy c?p `/` (Homepage) — gi?i thích HTML tr? v? ? `HomeController.Index()`.
  3. Truy c?p `/login` — m? `LoginController.LoginPage()` và gi?i thích form POST.
  4. Th?c hi?n login (demo POST): cho gi?ng viên xem `users.json` trong `Data/` và gi?i thích `JsonService.getInstance().getUsers()` (Singleton). Sau khi login thành công, show header `Set-Cookie: token=...` (server tr? v?).
  5. Truy c?p `/chat` — m? `ChatController.ChatList()` và gi?i thích tr?ng thái Online/Offline d?a trên `ChatService.lastActivity` (logic xóa history sau 3 phút).
  6. Vào `/chat/{id}` — show l?ch s? tin nh?n, g?i tin nh?n (POST) và gi?i thích `ChatService.AddMessage` c?p nh?t `lastActivity`.

- Nh?ng ?i?m c?n nêu rõ khi tr? l?i:
  - Dùng raw `Socket` (không dùng ASP.NET): lý do và cách parse HTTP th? công.
  - Singleton: vì sao `JsonService` c?n singleton (ch? 1 instance ??c file).
  - Builder: `RouteBuilder` dùng ?? ??ng ký route (show n?i g?i `.addHome().addLogin().addChat().build()` trong `Program.cs`).
  - Cookie: server l?u `token=username` qua header `Set-Cookie` và `HttpHelper.GetCookie` ??c cookie t? request.
  - X? lý tr?c ti?p route ??ng `/chat/{id}` trong `Program.cs` (gi?i thích vì sao không c?n router ??ng hoàn ch?nh).
  - Cách thay ??i timeout Online/Offline: vào `ChatService` s?a giá tr? `3` thành s? phút khác.

- N?u b? h?i chi ti?t: m? tr?c ti?p file t??ng ?ng và ch? vào ?o?n code. Tr? l?i ng?n g?n, mô t? m?c ?ích và dòng ho?t ??ng.

6. Academic Integrity (Trung th?c h?c thu?t)

- Không n?p code gi?ng/adapt quá m?c t? b?n khác ho?c do AI t?o hoàn toàn n?u b?n không hi?u.
- Các tr??ng h?p gi?ng nhau nhi?u kh? n?ng b? coi là vi ph?m và có th? b? 0 ?i?m ho?c x? lý k? lu?t.

7. Additional Notes & Checklist (Danh sách ki?m tra tr??c khi n?p)

- [ ] Ch?y `dotnet run` và demo 5 màn hình yêu c?u.
- [ ] ??m b?o `Data/users.json` có n?i dung ?úng và n?m t?i v? trí mà `JsonService` tìm ???c.
- [ ] Ch?p ?nh màn hình theo tên file quy ??nh và l?u vào `Results-screenshots`.
- [ ] Ch?p ?nh các ?o?n code Singleton và Builder vào `Code-DesignPatterns`.
- [ ] Ki?m tra `ProjectCode` bao g?m toàn b? mã ngu?n và file c?u hình (.csproj).
- [ ] Nén toàn b? (ZIP) v?i c?u trúc ?úng tr??c khi upload.

8. M?t s? l?nh h?u ích

- Ch?y project: `dotnet run` (trong th? m?c project ch?a `.csproj`).
- Build: `dotnet build`.
- ???ng d?n `users.json` n?u không tìm: ki?m tra `Data/users.json` ? root project ho?c `bin/Debug/net8.0/..`.

9. M?u tr? l?i ng?n khi gi?ng viên h?i (b?ng l?i):

- "Server b?t ??u ? `Program.cs` — dùng raw Socket, m?i k?t n?i x? lý trên Thread."
- "??c users t? `Data/users.json` b?ng `JsonService` (Singleton) ?? tránh ??c l?p và gi? nh?t quán."
- "Routes ???c ??ng ký b?ng `RouteBuilder` (Builder pattern). `/chat/{id}` x? lý ??ng trong `Program.cs` ?? d? tri?n khai."
- "Login t?o cookie `token=username` — server dùng `HttpHelper.GetCookie` ?? ki?m tra ??ng nh?p."

K?t lu?n: chu?n b? demo ch?y tr??c, s?p x?p ?nh và mã theo c?u trúc yêu c?u, và th?c hành tr? l?i ng?n g?n, ch? vào ?o?n code khi c?n gi?i thích chi ti?t.