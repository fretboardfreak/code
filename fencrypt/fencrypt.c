/*
 *
 * fencrypt.c
 *
 * Encrypt or decrypt a file with a passphrase.
 *
 * >$ cat inputfile | ./fencrypt "passphrase with spaces" > outputfile
 *
 * Written By: Curtis Sand, Copyright 2009
 *
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void decrypt (long *v, long *k){
    /* TEA decryption routine
     * 2 longs from v encrypted with 4 longs in k
     * answer is in v 
     */
    unsigned long n=32, sum, y=v[0], z=v[1];
    unsigned long delta=0x9e3779b9l;

	sum = delta<<5;
	while (n-- > 0){
		z -= (y<<4) + k[2] ^ y + sum ^ (y>>5) + k[3];
		y -= (z<<4) + k[0] ^ z + sum ^ (z>>5) + k[1];
		sum -= delta;
	}
	v[0] = y;
	v[1] = z;
}

void encrypt (long *v, long *k){
    /* TEA encryption algorithm 
     * 2 longs from v decrypted with 4 longs in k
     * answer is in v
     */
    unsigned long y = v[0], z=v[1], sum = 0;
    unsigned long delta = 0x9e3779b9, n=32;

	while (n-- > 0){
		sum += delta;
		y += (z<<4) + k[0] ^ z + sum ^ (z>>5) + k[1];
		z += (y<<4) + k[2] ^ y + sum ^ (y>>5) + k[3];
	}

	v[0] = y;
	v[1] = z;
}

void pack(int *a, int *b, long *l){
    *l = ((long)*a)<<8;
    *l += *b;
}

void unpack(int *a, int*b, long *l){
    *b = (int)(*l & 0x00FF);
    *a = (int)((*l & 0xFF00)>>8);
}

void printHelp(void){
    char *usage = "Usage:\n    >$ cat inputfile | ./fencrypt [-d/-h] \"passkey\" > outputfile";
    char *options = "Options:\n    -h : display this help\n    -d : decrypt instead of encrypt the data";
    char *desc = "fencrypt is a file encryptor/decryptor using TEA encryption with \n" \
                  "arbitrary length key.  Reads from stdin and prints to stdout.";

    printf("%s\n%s\n%s\n", desc, usage, options);
}

void getKeyArray(char *key, long *lkey){
    lkey[0] = 67;
    lkey[1] = 68;
    lkey[2] = 69;
    lkey[3] = 70;
}


int main(int argc, char *argv){


    /* key = 4 longs -> 8 ints,
     * if key is longer than 8 chars "1234567890"
     * use lsbits recursively until key is all used
     *
     * output = encrypt(encrypt(msg, "34567890"), "00000012")
     */

    char *key = "";

    // check command line parameters
    int decrypt = 0;
    if (argc != 2 && argc != 3){
        fprintf(stderr, "fencrypt: Error: bad cmd line arguments\n");
        return 1;
    }
    int i;
    for (i=0; i < argc; i++){
        if (strncmp(&argv[i],"-h", 2) == 0){
            printHelp();
            return 0;
        } else if (strncmp(&argv[i],"-d", 2) == 0){
            decrypt++;
            printf("fencrypt: decryption enabled\n");
        } else {
            *key = argv[i];
        }
    }

    printf("DEBUG: key = %s\n", key);
    long lkey[10];
    memset(lkey, 0, 10);
    getKeyArray(key, lkey);

    int endOfStdin = 0;
    while (!endOfStdin){
        int input[4], tmp;
        for(i = 0; i < 4; i++){
            if( (tmp = getchar()) == EOF){
                endOfStdin++;
                int j = i;
                for(j; j < 3; j++)
                    input[j]=0;
                input[3] = EOF;
                break;
            } else 
                input[i] = tmp;
        }
        long in[2] = {0, 0};
        pack(&input[0], &input[1], &in[0]);
        pack(&input[2], &input[3], &in[1]);
        encrypt(in, lkey);
        fprintf(stdout, "%ld%ld", in[0], in[1]);
    }
    
    return 0;
}

/* EOF cfile.c */
