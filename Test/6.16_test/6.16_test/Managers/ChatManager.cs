using System.Collections.Generic;
using _6._16_test.Models;

namespace _6._16_test.Managers
{
    /// <summary>
    /// [DESIGN PATTERN: SINGLETON]
    /// M?c ?ích: Ch? t?o DUY NH?T m?t ??i t??ng ChatManager trong su?t vòng ??i ?ng d?ng.
    /// T?i sao dùng ? ?ây: Vì danh sách các phòng chat c?n ???c dùng chung b?i t?t c? các Client/Thread khác nhau.
    /// N?u không dùng Singleton, m?i l?n g?i s? t?o m?i danh sách và làm m?t tin nh?n ?ã chat tr??c ?ó.
    /// </summary>
    internal class ChatManager
    {
        private static ChatManager instance = null;
        public List<ChatRoom> Rooms { get; private set; } = new List<ChatRoom>();

        // Constructor private: Ng?n ch?n vi?c dùng t? khóa 'new' t? bên ngoài class
        private ChatManager()
        {
            // Kh?i t?o 3 phòng chat m?c ??nh khi Object ???c t?o l?n ??u
            for (int i = 1; i <= 3; i++)
            {
                Rooms.Add(new ChatRoom { Id = i });
            }
        }

        // Ph??ng th?c t?nh ?? truy c?p instance duy nh?t
        public static ChatManager GetInstance()
        {
            if (instance == null)
            {
                instance = new ChatManager();
            }
            return instance;
        }

        public ChatRoom GetRoom(int id)
        {
            var room = Rooms.Find(r => r.Id == id);
            room?.CheckStatus(); // M?i l?n l?y phòng ??u check xem nó còn Online hay ?ã thành Offline
            return room;
        }
    }
}
