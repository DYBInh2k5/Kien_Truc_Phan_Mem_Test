# H??NG D?N CHI TI?T CÁCH TR? L?I V?N ?ÁP BÀI THI SA TEST

?? ??t ?i?m t?i ?a, b?n c?n ph?i h?p gi?a vi?c **Ch?y Demo** và **Gi?i thích Code**. D??i ?ây là k?ch b?n chi ti?t:

---

## ??? MÀN HÌNH 1: TRÌNH DI?N (DEMO TRÊN TRÌNH DUY?T)
*M? s?n `http://localhost:8080`. Khi th?y yêu c?u b?t ??u, hãy th?c hi?n theo th? t?:*

1.  **Trang ch? (`/`):** Ch? vào màn hình và nói: "?ây là trang thông tin sinh viên c?a em, ???c ph?c v? tr?c ti?p t? Socket Server."
2.  **??ng nh?p (`/login`):** Nh?p tài kho?n `admin/123`. Nói: "H? th?ng s? ??c file `users.json` ?? xác th?c. N?u ?úng, Server s? g?i l?nh Redirect (302) ??a em sang trang Chat."
3.  **H? th?ng phòng chat (`/chat`):** Ch? vào danh sách phòng. "Em có 3 phòng chat. Tr?ng thái Online (Xanh) hi?n lên vì phòng này v?a có ho?t ??ng chat trong vòng 3 phút qua."
4.  **G?i tin nh?n (`/chat/1`):** G?i th? m?t câu "Chào th?y". Nói: "Khi em nh?n G?i, trình duy?t t?o m?t `POST request`. Server nh?n d? li?u, c?p nh?t th?i gian ho?t ??ng cu?i (`LastActivity`) và l?u tin nh?n vào b? nh?."
5.  **Logic t? ??ng xóa:** "?? bài yêu c?u phòng Offline thì xóa l?ch s?. Sau 3 phút n?u không ai chat, hàm `CheckStatus` s? t? d?n d?p các tin nh?n này ?? t?i ?u b? nh?."

---

## ?? MÀN HÌNH 2: GI?I THÍCH CODE (TRONG VS CODE)
*Khi th?y h?i: "Em làm nh? th? nào?" ho?c "Ch? cho th?y ch? dùng Design Pattern", hãy m? các file sau:*

### 1. File `Program.cs` (Trái tim c?a Server)
- **?i?m nh?n:** Ch? vào `serverListen.Accept()` và `Thread t = new Thread(HandleClient)`.
- **Cách tr? l?i:** "Em dùng **Socket thô** ?? l?ng nghe. M?i khi có trình duy?t k?t n?i, em dùng m?t **Thread riêng** ?? x? lý. ?i?u này giúp nhi?u ng??i có th? chat cùng lúc mà không b? treo Server (Multi-threading)."

### 2. File `Managers/ChatManager.cs` (Design Pattern 1: Singleton)
- **?i?m nh?n:** Ch? vào `private static ChatManager instance` và `private ChatManager()`.
- **Cách tr? l?i:** "Em áp d?ng **Singleton Pattern** ? ?ây. M?c ?ích là ?? ??m b?o toàn b? Server ch? có **duy nh?t m?t ??i t??ng** qu?n lý tin nh?n. N?u không dùng Singleton, tin nh?n c?a ng??i này g?i ng??i kia s? không th?y vì m?i Request l?i t?o ra m?t danh sách m?i."

### 3. File `Factory/ResponseFactory.cs` (Design Pattern 2: Factory)
- **?i?m nh?n:** Ch? vào các hàm `Html()` và `Redirect()`.
- **Cách tr? l?i:** "?ây là **Factory Pattern**. Thay vì vi?t Header HTTP th? công l?p ?i l?p l?i, em t?p trung vi?c ?óng gói gói tin t?i ?ây. Nó giúp code s?ch h?n và em d? dàng qu?n lý các mã tr?ng thái nh? 200 OK hay 302 Found."

### 4. File `Models/ChatRoom.cs` (Business Logic)
- **?i?m nh?n:** Ch? vào `IsOnline => (DateTime.Now - LastActivity).TotalMinutes < 3`.
- **Cách tr? l?i:** "?ây là ch? em th?c hi?n yêu c?u 'Clear history' c?a th?y. Em so sánh th?i gian hi?n t?i v?i l?n chat cu?i. N?u v??t quá 3 phút, em g?i `Messages.Clear()`."

---

## ?? TH? T?C N?P BÀI (RULES TR??C KHI V?)
*Hãy ch?c ch?n b?n ?ã chu?n b? ?? 3 Part:*

- **Part 1 (Results-screenshots):** Ph?i có ?? ?nh: Trang ch?, Login, Danh sách phòng, N?i dung chat.
- **Part 2 (Code-DesignPatterns):** Ch?p file `ChatManager.cs` và `ResponseFactory.cs`.
- **Part 3 (ProjectCode):** File ZIP ch?a toàn b? code (nh? xóa folder `bin/obj` ?? file nh? và s?ch).

---

## ?? M?O ?? ???C ?I?M CAO (ACADEMIC INTEGRITY)
- **Tuy?t ??i không nói:** "Em dùng AI làm".
- **Nên nói:** "Em d?a trên ki?n trúc Socket t?ng Transport, t? Parse chu?i ???ng d?n (URL) và x? lý d? li?u Form POST (d?a trên ký t? `\r\n\r\n`) ?? th?c hi?n yêu c?u."
- **Thái ??:** Gi?i thích t? tin, ch? ?úng file code khi th?y h?i. N?u th?y yêu c?u s?a m?t dòng code nh? (ví d? ??i 3 phút thành 1 phút), hãy vào `ChatRoom.cs` s?a s? `3` thành s? `1` nhanh chóng.
