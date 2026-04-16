public static class Ex0302Top3DistinctParallel
{
    public static int[] FindTop3DistinctParallel(int[] arr)
    {
        if (arr is null)
            throw new ArgumentNullException(nameof(arr));

        return arr
            .AsParallel()
            .Distinct()
            .OrderByDescending(x => x)
            .Take(3)
            .ToArray();
    }

    public static void RunDemo()
    {
        var arr = new[] { 10, 4, 3, 50, 23, 90, 90, 50 };
        var top3 = FindTop3DistinctParallel(arr);

        Console.WriteLine("W03.02 - Top 3 distinct values (Parallel)");
        Console.WriteLine($"Input : [{string.Join(", ", arr)}]");
        Console.WriteLine($"Top 3 : [{string.Join(", ", top3)}]");
    }
}
