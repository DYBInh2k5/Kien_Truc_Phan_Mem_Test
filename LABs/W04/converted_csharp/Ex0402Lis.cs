public static class Ex0402Lis
{
    public static (int Length, List<int> Sequence) SolveLis(int[] arr)
    {
        if (arr is null || arr.Length == 0)
            return (0, new List<int>());

        var n = arr.Length;
        var dp = Enumerable.Repeat(1, n).ToArray();
        var prev = Enumerable.Repeat(-1, n).ToArray();

        for (var i = 1; i < n; i++)
        {
            for (var j = 0; j < i; j++)
            {
                if (arr[i] > arr[j] && dp[i] < dp[j] + 1)
                {
                    dp[i] = dp[j] + 1;
                    prev[i] = j;
                }
            }
        }

        var maxIdx = 0;
        for (var i = 1; i < n; i++)
        {
            if (dp[i] > dp[maxIdx])
                maxIdx = i;
        }

        var seq = new List<int>();
        for (var k = maxIdx; k != -1; k = prev[k])
            seq.Add(arr[k]);
        seq.Reverse();

        return (dp[maxIdx], seq);
    }

    public static void RunDemo()
    {
        var arr = new[] { 1, 3, 2, 4, 5 };
        var result = SolveLis(arr);

        Console.WriteLine("W04.02 - Longest Increasing Subsequence (LIS)");
        Console.WriteLine($"Input      : [{string.Join(", ", arr)}]");
        Console.WriteLine($"LIS Length : {result.Length}");
        Console.WriteLine($"LIS Seq    : [{string.Join(", ", result.Sequence)}]");
    }
}
