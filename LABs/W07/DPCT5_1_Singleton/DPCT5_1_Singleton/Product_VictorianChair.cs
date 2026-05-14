using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DPCP51_AbstractFactory
{
    internal class Product_VictorianChair : IProduct_Chair
    {
        public void hasLegs()
        {
            Console.WriteLine("Victorian: 4 legs");
        }
        public void sitOn()
        {
            Console.WriteLine("Victorian: siton");
        }
    }
}
