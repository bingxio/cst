#include <stdio.h>
#include <stdint.h>

uint8_t dt[8][3] = {
    {1,1,1}, {1,1,0}, {1,0,1}, {1,0,0},
    {0,1,1}, {0,1,0}, {0,0,1}, {0,0,0}
};

static inline char* f(uint8_t b) {
    return b == 1 ? "---" : "- -";
}

int main(int argc, char** argv) {
    char* n = *++argv;
    int x = *n++ - '1', y = *n++ - '1';
    int m = *n++ - '1';
    uint8_t l[8], c[8], r[8];

    for (int i = 0; i < 6; i++) {
        l[i] = i < 3 ? dt[y][i] : dt[x][i - 3];
    }
    for (int i = 0, j = 1; i < 3; i++) c[i] = l[j++];
    for (int i = 3, j = 2; i < 6; i++) c[i] = l[j++];
    for (int i = 0; i < 6; i++) {
        r[i] = i == m ? !l[i] : l[i];
    }
    for (int i = 5; i > -1; i--) {
        printf("  %s  %s  %s\n", f(l[i]), f(c[i]), f(r[i]));
    }
    return 0;
}
