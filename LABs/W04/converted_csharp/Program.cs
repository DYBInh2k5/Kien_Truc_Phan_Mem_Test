using System.Globalization;

Console.OutputEncoding = System.Text.Encoding.UTF8;
CultureInfo.DefaultThreadCurrentCulture = new CultureInfo("vi-VN");
CultureInfo.DefaultThreadCurrentUICulture = new CultureInfo("vi-VN");

while (true)
{
    Console.WriteLine("================ EXERCISES MENU ================");
    Console.WriteLine("1. W03.01 - Parallel: Largest value in array");
    Console.WriteLine("2. W03.02 - Parallel: Top 3 distinct values");
    Console.WriteLine("3. W04.01 - Ascending subsequences length > 2");
    Console.WriteLine("4. W04.02 - Longest Increasing Subsequence (LIS)");
    Console.WriteLine("5. W04.03 - Longest consecutive subsequence");
    Console.WriteLine("6. W05.A02 - Regex verify (email / CCCD / VN fullname)");
    Console.WriteLine("0. Exit");
    Console.Write("Choose: ");

    var choice = Console.ReadLine()?.Trim();
    Console.WriteLine();

    switch (choice)
    {
        case "1":
            Ex0301FindLargestParallel.RunDemo();
            break;
        case "2":
            Ex0302Top3DistinctParallel.RunDemo();
            break;
        case "3":
            Ex0401AscendingSubsequences.RunDemo();
            break;
        case "4":
            Ex0402Lis.RunDemo();
            break;
        case "5":
            Ex0403LongestConsecutive.RunDemo();
            break;
        case "6":
            Ex05A02RegexValidation.RunDemo();
            break;
        case "0":
            return;
        default:
            Console.WriteLine("Invalid choice. Please try again.");
            break;
    }

    Console.WriteLine("\nPress Enter to continue...");
    Console.ReadLine();
    Console.Clear();
}
