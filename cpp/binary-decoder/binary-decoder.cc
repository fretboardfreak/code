#include <stdio.h>

#include "binary-decoder.h"

void test_decoder(void){
    union decoder dcdr;
    dcdr.data = 0x12345678;
    printf("word.hi = 0x%x\n", dcdr.word.hi);
    printf("word.low = 0x%x\n", dcdr.word.low);
    printf("nibble.hh = 0x%x\n", dcdr.nibble.hh);
    printf("nibble.hl = 0x%x\n", dcdr.nibble.hl);
    printf("nibble.lh = 0x%x\n", dcdr.nibble.lh);
    printf("nibble.ll = 0x%x\n", dcdr.nibble.ll);
}

int main(int argc, char **argv){
    test_decoder();
}
