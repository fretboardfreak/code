#include <iostream>

#include "test.h"

using namespace std;

//void test_decoder(void){
//    union decoder dcdr;
//    dcdr.data = 0x12345678;
//    printf("word.hi = 0x%x\n", dcdr.word.hi);
//    printf("word.low = 0x%x\n", dcdr.word.low);
//    printf("nb.hh = 0x%x\n", dcdr.nb.hh);
//    printf("nb.hl = 0x%x\n", dcdr.nb.hl);
//    printf("nb.lh = 0x%x\n", dcdr.nb.lh);
//    printf("nb.ll = 0x%x\n", dcdr.nb.ll);
//}

Test::Test(int num) {
    data=num;
}

int Test::get_val(void){
    return data++;
}

int main(int argc, char **argv){
    int num=0;
    cout << "gimme a number: ";
    cin >> num;
    Test test_obj = Test(num);
    cout << "Value is " << test_obj.get_val() << endl;
    cout << "Value is now " << test_obj.get_val() << endl;
    return 0;
};
