#include <iostream>

#include "test.h"
#include <ctime>
#include <cstring>
#include <syslog.h>
#include <string>
#include <atomic>

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

typedef struct BLAH_S {
    int first, second;
} blah;

blah* foo(void){
    blah *myBlah = new blah{ 4, 5 };
    return myBlah;
}

class babar {
public:
    int x, y;

    babar(int a, int b):
        x(a),
        y(b)
    {
        cout << "testing " << a << " " << b << endl;
    }
};

typedef struct foo_s Foo_t;

int main(int argc, char **argv){

    string foo="foo";
    if (foo.compare("foo") == 0)
        cout << "SAME" << endl;

    babar b = babar(3, 7);

    Foo_t blah;

    return 0;
};
