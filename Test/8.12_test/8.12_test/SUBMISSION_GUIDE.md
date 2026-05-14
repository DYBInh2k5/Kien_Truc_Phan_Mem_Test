SA TEST - Submission & Viva Guide

M?c ?ích
- Tài li?u này mô t? chi ti?t quy ??nh n?p bài, c?u trúc th? m?c b?t bu?c và k?ch b?n trình bày (màn hình ch?y + code) ?? b?n chu?n b? v?n ?áp.

1) Attendance (Hi?n di?n)
- Ph?i có m?t t?i phòng Lab/l?p h?c trong bu?i n?p và v?n ?áp. V?ng không phép có th? d?n t?i không ???c ch?m.

2) Submission structure (C?u trúc n?p trên h? th?ng)
- B?t bu?c n?p ?úng 3 th? m?c ? root c?a zip:
  - `Results-screenshots` : 3-5 ?nh ch?p màn hình giao di?n ?ang ch?y (Home, Login success, Login fail, Chat room, Online/Offline).
  - `Code-DesignPatterns` : 3-5 ?nh ch?p ?o?n code minh h?a áp d?ng Design Patterns (Singleton, Builder).
  - `ProjectCode` : Toàn b? source code project (?i kèm folder `data`, `html`, `css` n?u có).
- Thi?u ho?c ??t sai tên folder s? ?nh h??ng ?i?m.

3) File naming (??t tên file b?ng ti?ng Anh ng?n g?n, rõ ràng)
- Ví d?: `login_success.png`, `chat_room_online.png`, `singleton_pattern.png`, `builder_pattern.png`, `project_source.zip`.

4) Ki?m tra ch?y ?ng d?ng (Application functionality)
- B?t bu?c ch?y ???c t?i `http://localhost:8080`.
- Các l?nh c? b?n (t? th? m?c project):
  - `dotnet build`
  - `dotnet run`
- M? Console: ki?m tra các log nh? `[SUCCESS] Loaded users from: ...` và `Number of accounts: 2`.

5) K?ch b?n trình bày (Màn hình ch?y + Màn hình code)
- Trình t? th?c hi?n khi trình bày:
  1. M? Console server, cho gi?ng viên xem log kh?i ??ng và log load `accounts.json`.
  2. M? trình duy?t: vào `http://localhost:8080` (Home page) — nói ng?n v? n?i dung trang.
  3. Click `Login` -> ?i?n `nntu` / `56789` -> submit. 
     - Trình bày: server t?o token và tr? `Set-Cookie`, trình duy?t redirect ??n `/chat`.
     - M? Developer Tools (Network/Storage) ?? cho gi?ng viên xem Header `Set-Cookie` và Cookie `token` ?ã ???c l?u.
  4. ? `/chat`: hi?n th? danh sách phòng cùng tr?ng thái `ONLINE`/`OFFLINE`. Gi?i thích: so sánh `Now - LastActivity <= 3 phút` ?? xác ??nh online.
  5. Vào 1 phòng (`/chat/1`): hi?n th? l?ch s? tin nh?n (time, username, message) và khung g?i tin. Th?c hi?n g?i 1 tin nh?n -> server nh?n POST -> c?p nh?t `LastActivity` -> redirect l?i ?? hi?n th? trang có tin nh?n m?i.
  6. Minh h?a phòng `OFFLINE` b?ng cách mô ph?ng (nêu cách ki?m tra ho?c s?a `LastActivity` t?m th?i) và cho th?y l?ch s? b? xóa.

6) Màn hình code c?n trình bày (và nh?ng n?i dung c?n gi?i thích ng?n g?n)
- `Program.cs`:
  - Mô t?: Socket server, l?ng nghe c?ng 8080, Accept connection, m?i connection kh?i 1 Thread.
  - Nêu cách parse HTTP: tách Header/Body b?ng `\r\n\r\n` ?? l?y Method, Path, Cookie và Body.
- `Router.cs`:
  - Mô t?: ?i?u h??ng các route: `/`, `/login` (GET/POST), `/chat`, `/chat/:id` (GET/POST).
  - Gi?i thích: cách x? lý Redirect (302) và cách set Cookie (`Set-Cookie` header).
- `JsonAccountSingleton.cs`:
  - Mô t?: Singleton ??c `data/accounts.json` m?t l?n, l?u vào `List<User>`.
  - Gi?i thích l?i ích: tránh ??c nhi?u l?n, d? li?u dùng chung gi?a các Thread.
- `ChatBuilder.cs`:
  - Mô t?: Builder t?o HTML cho trang chat (title, body, form).
  - Gi?i thích l?i ích: tách bi?t UI và logic, d? thay theme.
- `ChatRoom.cs`:
  - Mô t?: l?u `Messages`, `LastActivity` và hàm `IsOnline()` ki?m tra 3 phút và xóa l?ch s? khi offline.
- `User.cs`, `Message.cs`:
  - Model ??n gi?n cho d? li?u.

7) Các câu h?i hay g?p (và câu tr? l?i m?u ng?n g?n)
- Q: "Cookie token ???c t?o ? ?âu?" 
  - A: T?o trong `HandleLogin` (Guid.NewGuid()) và tr? header `Set-Cookie`.
- Q: "Làm sao server bi?t user ?ã ??ng nh?p?" 
  - A: D?a vào header `Cookie` g?i kèm; code ki?m tra s? t?n t?i `token=` (??n gi?n cho bài lab).
- Q: "Làm th? nào ?? xác ??nh phòng online?" 
  - A: So sánh `DateTime.Now - LastActivity <= TimeSpan.FromMinutes(3)`; n?u l?n h?n thì g?i `Messages.Clear()`.
- Q: "Ph?n parse HTTP có an toàn/hoàn ch?nh không?" 
  - A: ?ây là b?n mini-server ph?c v? h?c t?p: parse th? công ?? cho GET/POST form urlencoded; production c?n th? vi?n chu?n.
- Q: "Singleton thread-safe không?" 
  - A: Hi?n implementation là simple Singleton. Vì ch? ??c JSON m?t l?n lúc kh?i t?o, trong ng? c?nh lab này là ??; n?u c?n thread-safe có th? dùng lock ho?c Lazy<T>.

8) Academic Integrity (Liêm chính h?c thu?t)
- Không n?p code gi?ng ng??i khác. N?u bài gi?ng ho?c là s?n ph?m AI mà không hi?u, có th? b? 0 ?i?m.

9) Checklist tr??c khi n?p
- [ ] Build thành công (`dotnet build`).
- [ ] Server ch?y, truy c?p `http://localhost:8080` ???c.
- [ ] Ch?p ?nh màn hình theo yêu c?u và ??t tên ?úng.
- [ ] Ch?p ?nh code (Singleton, Builder) vào `Code-DesignPatterns`.
- [ ] ?óng gói `ProjectCode` cùng `data` folder.

10) Ghi chú k? thu?t ng?n (debug nhanh n?u không login)
- M? Console server, ki?m tra log "[SUCCESS] Loaded users" ho?c l?i file JSON.
- N?u log báo `accounts.json NOT FOUND`, ??m b?o file `data/accounts.json` có trong th? m?c build (project csproj ?ã c?u hình copy).
- Ki?m tra g?i form: developer tools -> Network -> ch?n request POST `/login` -> ki?m tra Request Payload và Response headers (Set-Cookie).


File này ?ã ???c t?o ?? in ho?c dán vào ph?n n?p bài làm tài li?u kèm theo. Chúc b?n v?n ?áp t?t và n?p bài thành công.