#ifndef _BINARY_DECODER
#define _BINARY_DECODER

#include <stdint.h>

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
    } nibble;
};

void test_decoder(void);

#endif /* _BINARY_DECODER */
