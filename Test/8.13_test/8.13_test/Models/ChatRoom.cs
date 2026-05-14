using System.Collections.Generic;

namespace SATestSocket.Models
{
    /// <summary>
    /// Model qu?n lý thông tin phòng chat.
    /// L?u tr? danh sách tin nh?n và th?i gian ho?t ??ng cu?i cùng ?? xác ??nh tr?ng thái Online/Offline.
    /// </summary>
    internal class ChatRoom
    {
        public int id { get; set; }

        // Danh sách l?u tr? l?ch s? tin nh?n trong phòng
        public List<Message> messages =
            new List<Message>();

        // Th?i ?i?m cu?i cùng có tin nh?n g?i t?i phòng này
        public DateTime lastActivity { get; set; }
    }
}
