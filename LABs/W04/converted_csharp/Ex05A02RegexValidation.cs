using System.Text.RegularExpressions;

public static class Ex05A02RegexValidation
{
    private static readonly Regex EmailRegex = new(@"^[\w.-]+@[\w.-]+\.\w+$", RegexOptions.Compiled);
    private static readonly Regex CccdRegex = new(@"^\d{12}$", RegexOptions.Compiled);
    private static readonly Regex VnFullNameRegex = new(
        @"^[A-ZÀ-Ỹ][a-zà-ỹ]+(\s[A-ZÀ-Ỹ][a-zà-ỹ]+)+$",
        RegexOptions.Compiled | RegexOptions.CultureInvariant);

    public static bool ValidateEmail(string value) => EmailRegex.IsMatch(value);

    public static bool ValidateCccd(string value) => CccdRegex.IsMatch(value);

    public static bool ValidateVnFullName(string value) => VnFullNameRegex.IsMatch(value);

    public static void RunDemo()
    {
        Console.WriteLine("W05.A02 - Regex verify (C#)");

        var email = Ask("Email");
        var cccd = Ask("CCCD (12 digits)");
        var fullName = Ask("VN fullname");

        Console.WriteLine();
        Console.WriteLine($"Email valid   : {ValidateEmail(email)}");
        Console.WriteLine($"CCCD valid    : {ValidateCccd(cccd)}");
        Console.WriteLine($"Fullname valid: {ValidateVnFullName(fullName)}");
    }

    private static string Ask(string label)
    {
        Console.Write($"Enter {label}: ");
        return Console.ReadLine()?.Trim() ?? string.Empty;
    }
}
