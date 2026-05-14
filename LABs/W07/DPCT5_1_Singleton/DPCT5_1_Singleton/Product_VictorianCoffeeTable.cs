using System;

namespace DPCP51_AbstractFactory
{
    internal class Product_VictorianCoffeeTable : IProduct_CoffeeTable
    {
        public void hasGlass()
        {
            Console.WriteLine("Victorian Coffee Table: No glass");
        }
    }
}
