#include <iostream>

void test1(int x)
{
    if (x == 1000)
        std::cout << "Jackpot!\n";
}

void test2(int x)
{
    if (x == 1000)
        std::cout << "Bingo!\n";
}

int main()
{
    std::cout << "Hello, world!\n";
    test1(1);
    test2(9);
    return 0;
}
