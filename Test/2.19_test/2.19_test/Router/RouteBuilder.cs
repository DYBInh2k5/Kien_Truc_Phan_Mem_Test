namespace SA_TEST.Router
{
    // Áp d?ng BUILDER PATTERN: Giúp c?u hình ???ng d?n (Route) cho ?ng d?ng m?t cách linh ho?t và m?ch l?c
    internal class RouteBuilder
    {
        private WebRouter router = new WebRouter();

        // Ph??ng th?c tr? v? 'this' (chính nó) ?? t?o ki?u g?i hàm n?i ti?p (Fluent Interface)
        public RouteBuilder addHome(Func<string> action)
        {
            router.addRoute("/", action); // Gán hàm x? lý cho trang ch?
            return this;
        }

        public RouteBuilder addLogin(Func<string> action)
        {
            router.addRoute("/login", action); // Gán hàm x? lý cho trang ??ng nh?p
            return this;
        }

        public RouteBuilder addChat(Func<string> action)
        {
            router.addRoute("/chat", action); // Gán hàm x? lý cho danh sách phòng chat
            return this;
        }

        // B??c hoàn t?t ?? nh?n v? ??i t??ng WebRouter ?ã ???c c?u hình xong
        public WebRouter build()
        {
            return router;
        }
    }
}
