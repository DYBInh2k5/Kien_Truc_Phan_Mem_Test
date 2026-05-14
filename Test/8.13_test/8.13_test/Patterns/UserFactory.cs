using SATestSocket.Models;

namespace SATestSocket.Patterns
{
    /// <summary>
    /// FACTORY PATTERN: L?p chuyên trách vi?c kh?i t?o ??i t??ng User.
    /// Giúp qu?n lý vi?c t?o m?i User m?t cách t?p trung và linh ho?t.
    /// </summary>
    internal class UserFactory
    {
        /// <summary>
        /// T?o m?t instance m?i c?a l?p User v?i tên ??ng nh?p và m?t kh?u.
        /// </summary>
        public static User create(
            string username,
            string password)
        {
            return new User
            {
                username = username,
                password = password
            };
        }
    }
}
