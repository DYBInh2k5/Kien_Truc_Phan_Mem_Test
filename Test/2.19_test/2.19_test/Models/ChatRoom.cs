using System.Collections.Generic;

namespace SA_TEST.Models
{
    // ??i t??ng ??i di?n cho m?t phòng chat
    internal class ChatRoom
    {
        public int id { get; set; } // ??nh danh phòng

        // Danh sách các tin nh?n trong phòng
        public List<Message> messages =
            new List<Message>();

        // Th?i ?i?m cu?i cùng có t??ng tác (?? tính Online/Offline)
        public DateTime lastActivity { get; set; }
    }
}
