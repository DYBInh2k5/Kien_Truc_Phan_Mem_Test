using System.Net;

namespace SA_TEST.Utils
{
    // L?p h? tr? các thao tác bóc tách d? li?u HTTP th? công
    internal class HttpHelper
    {
        // Phân tích d? li?u t? Body c?a Request (Dành cho POST form)
        public static Dictionary<string, string> ParseFormData(string requestData)
        {
            var dict = new Dictionary<string, string>();
            string[] separator = { "\r\n\r\n" };
            // Tách ph?n Header và Body b?ng dòng tr?ng kép
            var parts = requestData.Split(separator, StringSplitOptions.None);
            if (parts.Length < 2) return dict;

            // L?y ph?n body và lo?i b? các ký t? null ho?c kho?ng tr?ng th?a ? hai ??u
            var body = parts[1].Trim('\0').Trim();
            if (string.IsNullOrEmpty(body)) return dict;

            var pairs = body.Split('&'); // Tách các c?p key=value b?ng d?u &
            foreach (var pair in pairs)
            {
                var kv = pair.Split('=');
                if (kv.Length == 2) 
                {
                    // Gi?i mã URL và Trim ?? lo?i b? \r ho?c \n d? th?a t? browser
                    string key = WebUtility.UrlDecode(kv[0]).Trim();
                    string value = WebUtility.UrlDecode(kv[1]).Trim();
                    dict[key] = value;
                }
            }
            return dict;
        }

        // Tìm giá tr? c?a m?t Cookie c? th? trong Request
        public static string GetCookie(string requestData, string cookieName)
        {
            var lines = requestData.Split("\r\n");
            foreach (var line in lines)
            {
                if (line.StartsWith("Cookie:"))
                {
                    // Tách các cookie b?ng d?u ch?m ph?y
                    var cookies = line.Substring(7).Split(';');
                    foreach (var c in cookies)
                    {
                        var kv = c.Trim().Split('=');
                        if (kv.Length == 2 && kv[0] == cookieName) return kv[1];
                    }
                }
            }
            return null;
        }
    }
}
