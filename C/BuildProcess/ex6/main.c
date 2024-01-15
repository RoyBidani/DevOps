// main.c

#include <stdio.h>
#include "functions.h"

int main() {
    const char* str1 = "Hello";
    const char* str2 = "World";

    size_t len = StrLen(str1);
    printf("Length of str1: %zu\n", len);

    int cmp = StrCmp(str1, str2);
    if (cmp < 0) {
        printf("str1 is less than str2\n");
    } else if (cmp > 0) {
        printf("str1 is greater than str2\n");
    } else {
        printf("str1 is equal to str2\n");
    }

    return 0;
}

