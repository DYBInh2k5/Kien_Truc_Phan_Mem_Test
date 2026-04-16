class Full
{
    static void Main()
    {
        Console.WriteLine("Parallel Architecture !");

        int N = 10_000_000; // 10 triệu
        int[] data = new int[N];

        Random rand = new Random();

        // Generate random numbers
        for (int i = 0; i < N; i++)
        {
            data[i] = rand.Next(1, 1000000);
        }

        Console.WriteLine("Array generated!");

        // =============================
        // SEQUENTIAL
        // =============================

        Console.WriteLine("\nSequential Processing");

        int minSeq = int.MaxValue;
        int maxSeq = int.MinValue;

        for (int i = 0; i < N; i++)
        {
            if (data[i] < minSeq)
                minSeq = data[i];

            if (data[i] > maxSeq)
                maxSeq = data[i];
        }

        Console.WriteLine($"Sequential Min = {minSeq}");
        Console.WriteLine($"Sequential Max = {maxSeq}");

        // =============================
        // PARALLEL (WRONG - race condition)
        // =============================

        Console.WriteLine("\nParallel Processing (No Lock)");

        int minPar = int.MaxValue;
        int maxPar = int.MinValue;

        Parallel.For(0, N, i =>
        {
            if (data[i] < minPar)
                minPar = data[i];

            if (data[i] > maxPar)
                maxPar = data[i];
        });

        Console.WriteLine($"Parallel Min = {minPar}");
        Console.WriteLine($"Parallel Max = {maxPar}");

        // =============================
        // COMPARE
        // =============================

        Console.WriteLine("\nComparing Results...");

        if (minSeq != minPar || maxSeq != maxPar)
        {
            Console.WriteLine("Mismatch detected!");
        }
        else
        {
            Console.WriteLine("Results match!");
        }

        // =============================
        // PARALLEL CORRECT (WITH LOCK)
        // =============================

        Console.WriteLine("\nParallel Processing (With Lock)");

        int minCorrect = int.MaxValue;
        int maxCorrect = int.MinValue;

        object locker = new object();

        Parallel.For(0, N, i =>
        {
            lock (locker)
            {
                if (data[i] < minCorrect)
                    minCorrect = data[i];

                if (data[i] > maxCorrect)
                    maxCorrect = data[i];
            }
        });

        Console.WriteLine($"Correct Parallel Min = {minCorrect}");
        Console.WriteLine($"Correct Parallel Max = {maxCorrect}");

        Console.WriteLine("\nDone.");
    }
}