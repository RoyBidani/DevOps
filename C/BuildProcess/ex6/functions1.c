// function1.c
#include <stdio.h>
#include <assert.h>
#include "functions.h"

size_t StrLen(const char* str) {
    assert(str != NULL);
    size_t len = 0;
    while (*str != '\0') {
        ++len;
        ++str;
    }
    return len;
}



