namespace _8._12_test
{
    /// <summary>
    /// Model ??i di?n cho ng??i dùng (User) trong h? th?ng.
    /// Dùng ?? map d? li?u t? file JSON `accounts.json` thông qua th? vi?n `System.Text.Json`.
    /// Ch?a hai thu?c tính: `username` và `password`.
    /// </summary>
    public class User
    {
        public string username { get; set; }
        public string password { get; set; }
    }
}