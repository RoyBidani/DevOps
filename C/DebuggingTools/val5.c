#include <stdio.h>
#include <stdlib.h>

int main() {
    int* arr;  // Uninitialized pointer

    if (&arr == (int**)0x12345678) {
        printf("The pointer address matches the desired address.\n");
    } else {
        printf("The pointer address does not match the desired address.\n");
    }

    return 0;
}
