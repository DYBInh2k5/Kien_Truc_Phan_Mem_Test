using System;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Threading;
using System.Threading.Tasks;
using System.Diagnostics;

// ════════════════════════════════════════════════════
//  Models
// ════════════════════════════════════════════════════

class Product
{
    public int    Id    { get; set; }
    public string Name  { get; set; }
    public double Price { get; set; }
    public int    Stock { get; set; }
}

class OrderItem
{
    public Product Product  { get; set; }
    public int     Quantity { get; set; }
    public double  SubTotal => Product.Price * Quantity;
}

class Order
{
    public int            Id       { get; set; }
    public string         Customer { get; set; }
    public List<OrderItem> Items   { get; set; } = new();
    public double         Total    { get; private set; }
    public string         Status   { get; set; } = "Pending";

    // ① Tính tổng tiền của 1 order
    public void CalculateTotal()
    {
        Total = 0;
        foreach (var item in Items)
            Total += item.SubTotal;

        Console.WriteLine($"  [Thread {Thread.CurrentThread.ManagedThreadId}]" +
                          $" Order #{Id} ({Customer}) => Total: {Total:C}");
    }
}

// ════════════════════════════════════════════════════
//  Services
// ════════════════════════════════════════════════════

class ProductService
{
    private readonly List<Product> _catalog = new()
    {
        new Product { Id = 1, Name = "Laptop",   Price = 25_000_000, Stock = 10 },
        new Product { Id = 2, Name = "Mouse",    Price =    500_000, Stock = 50 },
        new Product { Id = 3, Name = "Keyboard", Price =    800_000, Stock = 30 },
        new Product { Id = 4, Name = "Monitor",  Price = 12_000_000, Stock =  5 },
        new Product { Id = 5, Name = "Headset",  Price =  1_200_000, Stock = 20 },
    };

    // ② Check tồn kho song song cho toàn bộ catalog
    public void CheckStockParallel()
    {
        Console.WriteLine("\n── Parallel stock check ──");
        var lowStock = new ConcurrentBag<Product>();

        Parallel.ForEach(_catalog, product =>
        {
            Console.WriteLine($"  [Thread {Thread.CurrentThread.ManagedThreadId}]" +
                              $" Checking stock: {product.Name} => {product.Stock} units");

            if (product.Stock < 10)
                lowStock.Add(product);
        });

        Console.WriteLine($"\n  ⚠  Low-stock products: {lowStock.Count}");
        foreach (var p in lowStock)
            Console.WriteLine($"     - {p.Name} (only {p.Stock} left)");
    }
}

class OrderService
{
    // ③ Xử lý nhiều order song song với Parallel.ForEach
    public void ProcessOrdersParallel(List<Order> orders)
    {
        Console.WriteLine("\n── Parallel.ForEach: calculating totals ──");

        Parallel.ForEach(orders, order =>
        {
            order.CalculateTotal();
            order.Status = "Calculated";
        });
    }

    // ④ Parallel.For — xử lý theo index
    public void ProcessOrdersParallelFor(List<Order> orders)
    {
        Console.WriteLine("\n── Parallel.For: processing by index ──");

        Parallel.For(0, orders.Count, i =>
        {
            var order = orders[i];
            Console.WriteLine($"  [Thread {Thread.CurrentThread.ManagedThreadId}]" +
                              $" Processing index {i} => Order #{order.Id}");
            order.Status = "Processed";
        });
    }

    // ⑤ PLINQ — tính tổng doanh thu bằng parallel query
    public double CalcTotalRevenuePLINQ(List<Order> orders)
    {
        Console.WriteLine("\n── PLINQ: sum revenue in parallel ──");

        double revenue = orders
            .AsParallel()
            .Where(o => o.Status == "Processed")
            .Sum(o => o.Total);

        Console.WriteLine($"  Total revenue (all orders): {revenue:C}");
        return revenue;
    }

    // ⑥ Task.WhenAll — gọi async song song (simulate I/O)
    public async Task ProcessOrdersAsync(List<Order> orders)
    {
        Console.WriteLine("\n── Task.WhenAll: async parallel ──");

        var tasks = orders.Select(order => Task.Run(() =>
        {
            Thread.Sleep(50); // simulate DB write
            order.Status = "Saved";
            Console.WriteLine($"  [Thread {Thread.CurrentThread.ManagedThreadId}]" +
                              $" Order #{order.Id} saved to DB");
        }));

        await Task.WhenAll(tasks);
        Console.WriteLine("  ✓ All orders saved.");
    }
}

// ════════════════════════════════════════════════════
//  Program
// ════════════════════════════════════════════════════

class Program
{
    static async Task Main()
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
        Console.WriteLine("╔══════════════════════════════════════════╗");
        Console.WriteLine("║  Parallel Order Processing — Demo        ║");
        Console.WriteLine("╚══════════════════════════════════════════╝");

        // ── seed data ──
        var product = new List<Product>
        {
            new Product { Id = 1, Name = "Laptop",   Price = 25_000_000, Stock = 10 },
            new Product { Id = 2, Name = "Mouse",    Price =    500_000, Stock = 50 },
            new Product { Id = 3, Name = "Keyboard", Price =    800_000, Stock = 30 },
        };

        var orders = new List<Order>
        {
            new Order { Id = 1, Customer = "An",
                Items = { new OrderItem { Product = product[0], Quantity = 1 },
                          new OrderItem { Product = product[1], Quantity = 2 } } },
            new Order { Id = 2, Customer = "Binh",
                Items = { new OrderItem { Product = product[1], Quantity = 3 },
                          new OrderItem { Product = product[2], Quantity = 1 } } },
            new Order { Id = 3, Customer = "Cuong",
                Items = { new OrderItem { Product = product[0], Quantity = 2 } } },
            new Order { Id = 4, Customer = "Dung",
                Items = { new OrderItem { Product = product[2], Quantity = 5 },
                          new OrderItem { Product = product[1], Quantity = 1 } } },
            new Order { Id = 5, Customer = "Em",
                Items = { new OrderItem { Product = product[0], Quantity = 1 },
                          new OrderItem { Product = product[2], Quantity = 2 } } },
        };

        var sw = Stopwatch.StartNew();

        // ── run demos ──
        var productSvc = new ProductService();
        var orderSvc   = new OrderService();

        productSvc.CheckStockParallel();          // ② stock check
        orderSvc.ProcessOrdersParallel(orders);   // ③ ForEach
        orderSvc.ProcessOrdersParallelFor(orders);// ④ For
        double revenue = orderSvc.CalcTotalRevenuePLINQ(orders); // ⑤ PLINQ
        await orderSvc.ProcessOrdersAsync(orders);// ⑥ async

        sw.Stop();
        Console.WriteLine($"\n╔══════════════════════════════════════════╗");
        Console.WriteLine($"║  Total revenue : {revenue,18:C}  ║");
        Console.WriteLine($"║  Elapsed       : {sw.ElapsedMilliseconds,15} ms     ║");
        Console.WriteLine($"║  CPU cores     : {Environment.ProcessorCount,15}        ║");
        Console.WriteLine($"╚══════════════════════════════════════════╝");
    }
}
