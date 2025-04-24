#include <iostream>
#include <fstream>

using namespace std;

int main()
{
    try
    {
        ofstream file("c_rand.txt");
        srand(time(NULL));
        for (int i = 0; i < 128; i++)
        {
            file << 0 + (rand() % 2);
        }
        file.close();
    }
    catch (const std::exception & ex)
    {
        std::cout << ex.what() << std::endl;
    }
}