#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
using namespace std;

/* decoder is a quick way to decode 32 bits of data into 8
 * bit chunks;
 */
union decoder {
    uint32_t data; // set this
    struct {
        uint16_t low;
        uint16_t hi;
    } word;
    struct {
        uint8_t ll;
        uint8_t lh;
        uint8_t hl;
        uint8_t hh;
    } nb;
};

int main(int argc, char **argv){

    union decoder dcdr;
    dcdr.data = 0x12345678;
    printf("word.hi = 0x%x\n", dcdr.word.hi);
    printf("word.low = 0x%x\n", dcdr.word.low);
    printf("nb.hh = 0x%x\n", dcdr.nb.hh);
    printf("nb.hl = 0x%x\n", dcdr.nb.hl);
    printf("nb.lh = 0x%x\n", dcdr.nb.lh);
    printf("nb.ll = 0x%x\n", dcdr.nb.ll);
    //uint32_t a;
    //uint8_t *b;

    //a = 0x12345678;
    //b = (uint8_t *) &a;

    //printf("a = 0x%x\n", a);
    //printf("*b = 0x%x\n", *b);
    //b += 1;
    //printf("*b = 0x%x\n", *b);


    return 0;
};
