using System;
using System.Threading.Tasks;

class Minmax
{
    static void Main()
    {
        int N = 10_000_000; // 10 million
        int[] data = new int[N];

        Random rand = new Random();

        // Generate random integers
        for (int i = 0; i < N; i++)
        {
            data[i] = rand.Next(1, 1000000);
        }

        Console.WriteLine("Array generated!");

        // =============================
        // Sequential
        // =============================
        int minSeq = int.MaxValue;
        int maxSeq = int.MinValue;

        for (int i = 0; i < N; i++)
        {
            if (data[i] < minSeq)
                minSeq = data[i];

            if (data[i] > maxSeq)
                maxSeq = data[i];
        }

        Console.WriteLine("\nSequential Result:");
        Console.WriteLine($"Min = {minSeq}");
        Console.WriteLine($"Max = {maxSeq}");

        // =============================
        // Parallel
        // =============================
        int minPar = int.MaxValue;
        int maxPar = int.MinValue;

        Parallel.For(0, N, i =>
        {
            if (data[i] < minPar)
                minPar = data[i];

            if (data[i] > maxPar)
                maxPar = data[i];
        });

        Console.WriteLine("\nParallel Result:");
        Console.WriteLine($"Min = {minPar}");
        Console.WriteLine($"Max = {maxPar}");

        // =============================
        // Compare
        // =============================
        Console.WriteLine("\nCompare:");

        if (minSeq == minPar && maxSeq == maxPar)
        {
            Console.WriteLine("Results MATCH");
        }
        else
        {
            Console.WriteLine("Results MISMATCH");
            Console.WriteLine("Possible cause: Race condition due to shared variables without synchronization.");
        }
    }
}