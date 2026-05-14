using System;

namespace DPCP51_AbstractFactory
{
    internal class Product_ModernSofa : IProduct_Sofa
    {
        public void hasCushions()
        {
            Console.WriteLine("Modern Sofa: 4 cushions");
        }
    }
}
