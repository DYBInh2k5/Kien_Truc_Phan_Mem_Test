using System.Text.Json;
using SA_TEST.Models;

namespace SA_TEST.Services
{
    // Áp d?ng SINGLETON PATTERN: ??m b?o ch? có 1 th?c th? (instance) duy nh?t x? lý file d? li?u
    internal class JsonService
    {
        private static JsonService instance = null;

        // ??nh ngh?a Constructor là private ?? ng?n ch?n vi?c t?o ??i t??ng b?ng t? khóa 'new' t? bên ngoài
        private JsonService() { }

        // Ph??ng th?c t?nh ?? truy c?p vào th?c th? duy nh?t c?a l?p này
        public static JsonService getInstance()
        {
            if (instance == null)
            {
                instance = new JsonService();
            }

            return instance;
        }

        // Hàm ??c danh sách ng??i dùng t? file JSON
        public List<User> getUsers()
        {
            // Ki?m tra nhi?u v? trí ?? tìm file users.json (phòng tr??ng h?p ch?y t? Visual Studio ho?c dòng l?nh)
            string[] possiblePaths = {
                Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Data", "users.json"),
                Path.Combine(Directory.GetCurrentDirectory(), "Data", "users.json"),
                "Data/users.json",
                // Lùi 3 c?p th? m?c ?? tìm v? th? m?c g?c n?u ?ang ch?y trong bin/Debug/net8.0
                Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "Data", "users.json")
            };

            string path = "";
            foreach (var p in possiblePaths)
            {
                if (File.Exists(p))
                {
                    path = p;
                    break;
                }
            }

            if (string.IsNullOrEmpty(path))
            {
                Console.WriteLine("L?I: Không tìm th?y file users.json t?i b?t k? v? trí nào!");
                return new List<User>();
            }

            // ??c n?i dung v?n b?n thô t? file JSON
            string json = File.ReadAllText(path).Trim();
            try {
                // Chuy?n ??i ??nh d?ng v?n b?n JSON thành danh sách ??i t??ng User trong C#
                return JsonSerializer.Deserialize<List<User>>(json);
            } catch (Exception ex) {
                Console.WriteLine("L?I phân tích JSON: " + ex.Message);
                return new List<User>();
            }
        }
    }
}
