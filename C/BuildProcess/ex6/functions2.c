// function2.c
#include <stdio.h>
#include <assert.h>
#include "functions.h"

int StrCmp(const char* str1, const char* str2) {
    assert(str1 != NULL && str2 != NULL);
    while (*str1 == *str2) {
        if (*str1 == '\0') {
            return 0;
        }
        ++str1;
        ++str2;
    }
    return (*str1 < *str2) ? -1 : 1;
}
