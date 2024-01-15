#include <stdio.h>

int main() {
    const char * str1 = NULL;
    char const * str2;
    char * const str3 = NULL;
    char* str4 = NULL;
    char* const str5;

    str1 = str2;
    str2 = str3;
    str4 = str3;
    str3 = str4;
    str2 = str4;
    str4 = str2;
    str5 = str4;

    return 0;
}
