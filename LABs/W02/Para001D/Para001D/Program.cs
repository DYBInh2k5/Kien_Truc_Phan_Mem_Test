Console.WriteLine("Parallel Architecture !");

long i, N = 1000000000;

// Tuần Tự
Console.WriteLine("\n\n VD Tuan Tu: ");
double TongTT = 0;
for (i = 0; i <= N; i++)
{
    //Console.Write($"\t {i}");
    TongTT += i * i * i / 5.5;
}
Console.WriteLine($"\n... KQ Tuan Tu - TongTT = {TongTT}");

// Song Song 
Console.WriteLine("\n\n VD Song Song: ");
double TongSS = 0;
Parallel.For(0, N + 1, ii =>
{
    //Console.Write($"\t {ii}");
    TongSS += ii * ii * ii / 5.5;
});
Console.WriteLine($"\n... KQ Song Song - TongSS = {TongSS}");