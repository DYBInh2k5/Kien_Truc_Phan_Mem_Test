using SA_TEST.Services;

namespace SA_TEST.Controllers
{
    // L?p Controller qu?n lý trang ??ng nh?p
    internal class LoginController
    {
        // Tr? v? chu?i HTML ch?a Form ??ng nh?p
        public static string LoginPage()
        {
            return @"
            <html>
            <head>
                <link rel='stylesheet' href='/style.css'>
            </head>
            <body>

            <form method='POST' action='/login'>
                <h2>Login</h2>
                Username:
                <input name='username'/>

                <br/><br/>

                Password:
                <input name='password' type='password'/>

                <br/><br/>

                <button type='submit'>Login</button>

            </form>

            </body>
            </html>
            ";
        }
    }
}
