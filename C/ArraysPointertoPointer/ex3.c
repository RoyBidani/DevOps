#include <stdio.h>

int main() {
    printf("Size of int: %zu bytes\n", sizeof(int));
    printf("Size of char: %zu bytes\n", sizeof(char));
    printf("Size of float: %zu bytes\n", sizeof(float));
    printf("Size of double: %zu bytes\n", sizeof(double));
    printf("Size of void: %zu bytes\n", sizeof(void));
    printf("Size of short: %zu bytes\n", sizeof(short));
    printf("Size of long: %zu bytes\n", sizeof(long));
    printf("Size of unsigned int: %zu bytes\n", sizeof(unsigned int));
    printf("Size of unsigned char: %zu bytes\n", sizeof(unsigned char));
    printf("Size of signed int: %zu bytes\n", sizeof(signed int));
    printf("Size of signed char: %zu bytes\n", sizeof(signed char));
    printf("Size of long long: %zu bytes\n", sizeof(long long));

    return 0;
}

