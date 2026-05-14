using System;

namespace DPCP51_AbstractFactory
{
    internal class Product_VictorianSofa : IProduct_Sofa
    {
        public void hasCushions()
        {
            Console.WriteLine("Victorian Sofa: 2 cushions");
        }
    }
}
