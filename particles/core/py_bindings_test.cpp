#include <bits/stdc++.h>
using namespace std;

class Bonk 
{
    public:
        int add(int a, int b)
        {
            return privAdd(a,b);
        }

    private:
        int privAdd(int a, int b)
        {
            return a + b;
        }
};

extern "C" { 
    Bonk* Bonk_new() { return new Bonk(); } 
    int Bonk_add(Bonk* bonk, int a, int b) { return bonk->add(a, b); }
}

int main()
{
    Bonk b;
    cout << b.add(2,3) << endl;

    return 0;
}