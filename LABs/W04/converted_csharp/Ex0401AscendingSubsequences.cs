using System.Collections.Concurrent;

public static class Ex0401AscendingSubsequences
{
    public static List<List<int>> FindAllAscendingSubsequencesLengthGt2(int[] arr)
    {
        if (arr is null)
            throw new ArgumentNullException(nameof(arr));

        var bag = new ConcurrentBag<List<int>>();

        Parallel.For(0, arr.Length, start =>
        {
            var current = new List<int> { arr[start] };
            Backtrack(arr, start + 1, current, bag);
        });

        // De-duplicate by value sequence, then sort for stable output.
        return bag
            .GroupBy(seq => string.Join(",", seq))
            .Select(g => g.First())
            .OrderBy(seq => seq.Count)
            .ThenBy(seq => string.Join(",", seq))
            .ToList();
    }

    private static void Backtrack(int[] arr, int nextIndex, List<int> current, ConcurrentBag<List<int>> output)
    {
        if (current.Count >= 3)
            output.Add(new List<int>(current));

        for (var i = nextIndex; i < arr.Length; i++)
        {
            if (arr[i] > current[^1])
            {
                current.Add(arr[i]);
                Backtrack(arr, i + 1, current, output);
                current.RemoveAt(current.Count - 1);
            }
        }
    }

    public static void RunDemo()
    {
        var arr = new[] { 1, 3, 2, 4 };
        var subsequences = FindAllAscendingSubsequencesLengthGt2(arr);

        Console.WriteLine("W04.01 - Ascending subsequences with length > 2");
        Console.WriteLine($"Input : [{string.Join(", ", arr)}]");
        Console.WriteLine($"Count : {subsequences.Count}");
        Console.WriteLine("Results:");

        foreach (var seq in subsequences)
            Console.WriteLine($"- [{string.Join(", ", seq)}]");
    }
}
