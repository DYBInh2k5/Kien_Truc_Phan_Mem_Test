namespace SA_TEST.Controllers
{
    // L?p Controller qu?n lý trang ch?
    internal class HomeController
    {
        // Tr? v? chu?i HTML hi?n th? thông tin sinh viên
        public static string Index()
        {
            return @"
            <html>
            <head>
                <link rel='stylesheet' href='/style.css'>
            </head>
            <body>
                <h1>Student Information</h1>

                <p>ID: 2212345</p>
                <p>Fullname: Nguyen Van A</p>
                <p>PC: PC01</p>

                <a href='/login'>Login</a>

            </body>
            </html>
            ";
        }
    }
}
