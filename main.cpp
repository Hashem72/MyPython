#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

int main(int argc, char *argv[])
{
    ifstream f(argv[1]);
    if (! f.good())
    {
        cerr << "couldn't open file\n";
        //::exit(1);
    }

    std::string other1, other2, trash;
    unsigned a1, b1, a2, b2;

    while (f.peek() == '#')
    {
        std::getline(f, trash);
        //std::cout << trash << '\n';
    }
    f >> other1 >> a1 >> b1;
    std::getline(f, trash);
    unsigned counter(0);
    unsigned counter1(0);
    while (f.peek() == '#')
    {
        std::getline(f, trash);
        //std::cout << trash << '\n';
    }
    while(f >> other2 >> a2 >> b2)
    {
        std::getline(f, trash);
        if (b1 != a2)
        {
            std::cout << other1 << ' ' << a1 << ' ' << b1 << '\n';
            std::cout << other2 << ' ' << a2 << ' ' << b2 << '\n';
            counter1++;
        }
        other1 = other2;
        a1 = a2;
        b1 = b2;
        while (f.peek() == '#')
        {
            std::getline(f, trash);
            //std::cout << trash << '\n';
        }
        counter++;
    }
    std::cout << "read " << (counter+1) << " lines\n";
    std::cout << "read " << counter1 << " non adjacent lines\n";
    
    return 0;
}
