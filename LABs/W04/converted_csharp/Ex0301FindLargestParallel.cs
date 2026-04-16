public static class Ex0301FindLargestParallel
{
    public static int FindMaxParallel(int[] arr)
    {
        if (arr is null || arr.Length == 0)
            throw new ArgumentException("Array must not be null or empty.");

        var globalMax = int.MinValue;
        var gate = new object();

        Parallel.ForEach(
            source: arr,
            localInit: () => int.MinValue,
            body: (value, _, localMax) => value > localMax ? value : localMax,
            localFinally: localMax =>
            {
                lock (gate)
                {
                    if (localMax > globalMax)
                        globalMax = localMax;
                }
            });

        return globalMax;
    }

    public static void RunDemo()
    {
        var arr = new[] { 5, 8, 2, 10, 3, 99, 23, 44 };
        var max = FindMaxParallel(arr);

        Console.WriteLine("W03.01 - Largest value in array (Parallel)");
        Console.WriteLine($"Input : [{string.Join(", ", arr)}]");
        Console.WriteLine($"Max   : {max}");
    }
}
