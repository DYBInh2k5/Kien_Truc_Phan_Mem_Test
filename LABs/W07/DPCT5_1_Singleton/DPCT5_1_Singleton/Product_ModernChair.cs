using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DPCP51_AbstractFactory
{
    internal class Product_ModernChair : IProduct_Chair
    {
        public void hasLegs()
        {
            Console.WriteLine("Modern: 2 legs");
        }
        public void sitOn()
        {
            Console.WriteLine("Modern: siton");
        }
    }
}
