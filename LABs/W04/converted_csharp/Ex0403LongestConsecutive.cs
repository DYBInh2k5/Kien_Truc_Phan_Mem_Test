public static class Ex0403LongestConsecutive
{
    public static (int Length, List<int> Sequence) Solve(int[] arr)
    {
        if (arr is null || arr.Length == 0)
            return (0, new List<int>());

        var set = arr.ToHashSet();
        var bestLength = 0;
        var bestStart = 0;

        foreach (var num in set)
        {
            if (set.Contains(num - 1))
                continue;

            var current = num;
            var count = 1;
            while (set.Contains(current + 1))
            {
                current++;
                count++;
            }

            if (count > bestLength)
            {
                bestLength = count;
                bestStart = num;
            }
        }

        var sequence = Enumerable.Range(bestStart, bestLength).ToList();
        return (bestLength, sequence);
    }

    public static void RunDemo()
    {
        var arr = new[] { 1, 9, 3, 10, 4, 20, 2 };
        var result = Solve(arr);

        Console.WriteLine("W04.03 - Longest consecutive subsequence");
        Console.WriteLine($"Input        : [{string.Join(", ", arr)}]");
        Console.WriteLine($"Best length  : {result.Length}");
        Console.WriteLine($"Best sequence: [{string.Join(", ", result.Sequence)}]");
    }
}
