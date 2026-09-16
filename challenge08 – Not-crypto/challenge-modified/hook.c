#include <stdio.h>
#include <string.h>

int memcmp(const void *s1, const void *s2, size_t n) {
    printf("HOOKED MEMCMP!\n");
    return 0;
}
