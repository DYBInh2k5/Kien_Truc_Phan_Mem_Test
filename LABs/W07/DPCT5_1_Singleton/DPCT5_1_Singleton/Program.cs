using DPCP51_AbstractFactory;

Console.WriteLine("Design Patterns ! Creational Patterns - Abstract Factory");

IFactory ceo01, ceo02;

ceo01 = new Factory_Modern();
ceo02 = new Factory_Victorian();

IProduct_Chair xChair;

xChair = ceo01.createChair();
xChair.hasLegs();
xChair.sitOn();

xChair = ceo02.createChair();
xChair.hasLegs();
xChair.sitOn();

IProduct_CoffeeTable coffeeTable;
IProduct_Sofa sofa;

coffeeTable = ceo02.createCoffeeTable();
coffeeTable.hasGlass();

sofa = ceo02.createSofa();
sofa.hasCushions();

coffeeTable = ceo01.createCoffeeTable();
coffeeTable.hasGlass();

sofa = ceo01.createSofa();
sofa.hasCushions();
