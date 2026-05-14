H??NG D?N TR? L?I & TRÌNH BÀY (KHI M? MÀN HÌNH CH?Y + CODE)

M?c tiêu: minh h?a nhanh t?ng yêu c?u c?a ?? và tr? l?i các câu h?i gi?ng viên.

1) B? c?c màn hình (g?i ý)
- Trình duy?t (ph?i hi?n th? http://localhost:8080) ? bên ph?i.
- Console server (hi?n request/raw) ? d??i cùng ho?c bên trái d??i.
- Editor m? `Program.cs`, `Patterns/ServerFacade.cs`, `Patterns/UserFactory.cs` ? bên trái trên.

2) K?ch b?n demo (th?c hi?n t?ng b??c, nói ng?n 1 câu m?i b??c)
- B1: M? `http://localhost:8080` -> "?ây là trang ch?: ID, fullname, PC number, link Login." (show)
- B2: Click `Login` -> "Trang login (GET /login)" (show source form trong HTML string)
- B3: Nh?p `nntu` / `56789` -> Submit -> "POST /login: server ??c `users.json`, ki?m tra credentials, tr? v? Redirect 302 -> /chat" (show console request và redirect headers)
- B4: Trên `/chat`: hi?n th? danh sách phòng (online/offline) -> "Online n?u có ho?t ??ng trong 3 phút, n?u offline thì `messages.Clear()`" (m? `Program.cs` dòng x? lý)
- B5: Vào `/chat/1`, g?i tin nh?n -> "POST /chat/1: server l?u message vào memory, c?p nh?t `lastActivity`, redirect v? GET /chat/1 và hi?n th? l?ch s?" (show console log và n?i dung chat)

3) Các ?i?m c?n nh?n m?nh (ng?n g?n)
- Raw Socket + Thread: `Socket`, `Accept()`, m?i client x? lý trên `Thread` riêng (ghi ra console).
- HTTP th? công: parse dòng ??u, parse body `application/x-www-form-urlencoded` b?ng `ParseFormUrlEncoded()`.
- L?u user: JSON file `Data/users.json` (code có logic tìm file và ??c b?ng `System.Text.Json`).
- Design patterns: `UserFactory` (Factory) và `ServerFacade` (Facade) — m? file và ch? vào ph??ng th?c chính.

4) Câu h?i th??ng g?p và câu tr? l?i ng?n m?u
- Q: "Làm sao server x? lý nhi?u client?" ? A: "M?i k?t n?i `Accept()` ???c x? lý trên Thread m?i (không block vòng l?p chính)."
- Q: "Làm sao parse POST form?" ? A: "??c body raw, g?i `ParseFormUrlEncoded` tách `key=value`."
- Q: "Vì sao không dùng ASP.NET?" ? A: "Yêu c?u ?? yêu c?u s? d?ng Socket/TcpListener và HTTP th? công ?? h?c low-level networking."
- Q: "File users.json không tìm ???c?" ? A: "Code có c? ch? tìm nhi?u ???ng d?n t??ng ??i/scan toàn b? th? m?c hi?n hành; hãy ??m b?o `ProjectCode/Data/users.json` có trong n?p bài." 

5) Checklist nhanh tr??c khi trình bày (30s ki?m tra)
- [ ] Ch?y `dotnet run --project 8.13_test/8.13_test.csproj` thành công.
- [ ] Trình duy?t m? `http://localhost:8080` và các route: `/`, `/login`, `/chat`, `/chat/1` ho?t ??ng.
- [ ] `Data/users.json` có trong folder `ProjectCode/Data` trong file n?p.
- [ ] Có 3–5 screenshot trong `Results-screenshots` và code pattern trong `Code-DesignPatterns`.

6) M?o trình bày mi?ng
- Nói ng?n, ??nh h??ng: m?c tiêu ? cách ho?t ??ng ? demo t?ng route ? gi?i thích pattern.
- N?u b? yêu c?u s?a nhanh: m? console, chèn thêm Console.WriteLine ?? in request/paths, s?a trong `Program.cs` và l?u ?? server in thêm thông tin.

K?t lu?n: dùng file này làm k?ch b?n 3–5 phút. Gi? bình t?nh, m? console ?? minh h?a request raw khi c?n ch?ng minh parsing/redirect/??c JSON.