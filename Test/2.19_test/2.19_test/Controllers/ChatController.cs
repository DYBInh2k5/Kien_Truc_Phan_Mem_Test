using SA_TEST.Models;
using SA_TEST.Services;
using System.Text;

namespace SA_TEST.Controllers
{
    // L?p Controller qu?n lý các tính n?ng Chat
    internal class ChatController
    {
        // Hi?n th? danh sách các phòng chat kèm tr?ng thái Online/Offline
        public static string ChatList()
        {
            var rooms = ChatService.GetRooms();
            StringBuilder sb = new StringBuilder();
            sb.Append("<html><head><link rel='stylesheet' href='/style.css'></head><body><h1>Chat Rooms</h1><ul>");
            foreach (var room in rooms)
            {
                // Ki?m tra tr?ng thái d?a trên th?i gian ho?t ??ng cu?i cùng (3 phút)
                bool isOnline = (DateTime.Now - room.lastActivity).TotalMinutes <= 3;
                string status = isOnline ? "<span style='color:green'>Online</span>" : "<span style='color:red'>Offline</span>";
                sb.Append($"<li>Room {room.id} - {status} <a href='/chat/{room.id}'>Enter</a></li>");
            }
            sb.Append("</ul><a href='/'>Back Home</a></body></html>");
            return sb.ToString();
        }

        // Hi?n th? l?ch s? tin nh?n và form g?i tin nh?n cho m?t phòng c? th?
        public static string ChatRoom(int id)
        {
            var room = ChatService.GetRoom(id);
            if (room == null) return "<h1>Room not found</h1>";

            StringBuilder sb = new StringBuilder();
            sb.Append($"<html><head><link rel='stylesheet' href='/style.css'></head><body><h1>Room {id}</h1>");
            sb.Append("<div style='height:300px;overflow-y:scroll;border:1px solid #ccc;padding:10px;margin-bottom:10px;'>");
            foreach (var msg in room.messages)
            {
                // Render t?ng tin nh?n trong phòng
                sb.Append($"<p>[{msg.time:T}] <b>{msg.username}</b>: {msg.content}</p>");
            }
            sb.Append("</div>");
            sb.Append($"<form method='POST' action='/chat/{id}'>");
            sb.Append("<input name='message' placeholder='Type a message...' required />");
            sb.Append("<button type='submit'>Send</button>");
            sb.Append("</form>");
            sb.Append("<a href='/chat'>Back to Rooms</a></body></html>");
            return sb.ToString();
        }
    }
}
