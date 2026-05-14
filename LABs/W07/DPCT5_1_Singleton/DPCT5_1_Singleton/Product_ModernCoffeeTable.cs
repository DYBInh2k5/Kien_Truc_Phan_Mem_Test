using System;

namespace DPCP51_AbstractFactory
{
    internal class Product_ModernCoffeeTable : IProduct_CoffeeTable
    {
        public void hasGlass()
        {
            Console.WriteLine("Modern Coffee Table: Has glass");
        }
    }
}
