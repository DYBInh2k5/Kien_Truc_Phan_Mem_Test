namespace SA_TEST.Router
{
    // L?p qu?n lý danh sách các Route (URL) c?a ?ng d?ng
    internal class WebRouter
    {
        // Dictionary l?u tr? c?p [???ng d?n, Hàm th?c thi]
        public Dictionary<string, Func<string>> routes =
            new Dictionary<string, Func<string>>();

        // Thêm m?t route m?i vào h? th?ng
        public void addRoute(string url, Func<string> action)
        {
            routes[url] = action;
        }
    }
}
