using SA_TEST.Models;

namespace SA_TEST.Services
{
    // L?p qu?n lý logic c?a phòng chat và tin nh?n
    internal class ChatService
    {
        // Danh sách các phòng chat ???c l?u trong b? nh? (S? m?t khi t?t server)
        private static List<ChatRoom> rooms = new List<ChatRoom>
        {
            new ChatRoom { id = 1, lastActivity = DateTime.Now },
            new ChatRoom { id = 2, lastActivity = DateTime.Now.AddMinutes(-5) }
        };

        public static List<ChatRoom> GetRooms()
        {
            foreach (var room in rooms)
            {
                // LOGIC QUAN TR?NG: N?u quá 3 phút không ho?t ??ng, xóa toàn b? l?ch s? chat
                if ((DateTime.Now - room.lastActivity).TotalMinutes > 3)
                {
                    room.messages.Clear();
                }
            }
            return rooms;
        }

        public static ChatRoom GetRoom(int id)
        {
            var room = rooms.FirstOrDefault(r => r.id == id);
            // Ki?m tra t??ng t? cho t?ng phòng c? th?
            if (room != null && (DateTime.Now - room.lastActivity).TotalMinutes > 3)
            {
                room.messages.Clear();
            }
            return room;
        }

        public static void AddMessage(int roomId, string username, string content)
        {
            var room = rooms.FirstOrDefault(r => r.id == roomId);
            if (room != null)
            {
                // Thêm tin nh?n và c?p nh?t th?i gian ho?t ??ng m?i nh?t
                room.messages.Add(new Message { username = username, content = content, time = DateTime.Now });
                room.lastActivity = DateTime.Now;
            }
        }
    }
}
