#include <iostream>

#include "test.h"

using namespace std;
using namespace foobar;

Test::Test(int num)
{ data=num; }

int
Test::get_val(void)
{ return data++; }

Foo::Foo(): Test(99)
{};

int
Foo::get_val()
{ return 999; }

int main(int argc, char **argv){
    int num=0;
    cout << "gimme a number: ";
    cin >> num;
    Test test_obj = Test(num);
    cout << "Value is " << test_obj.get_val() << endl;
    cout << "Value is now " << test_obj.get_val() << endl;
    cout << "Banana is " << banana.get_val() << endl;

    return 0;
};
