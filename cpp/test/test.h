#ifndef _TEST_H
#define _TEST_H

namespace foobar {
    class Test {
        public:
            Test(int num);
            virtual int get_val();
        private:
            int data;
    };

    struct Foo : public Test {
        Foo();
        int get_val();
    } banana;

};

#endif //_TEST_H
