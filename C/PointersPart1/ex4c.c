
/*
the function swaps() is designed to swap values pointed to by two pointers, not the pointers themselves. to swap two pointers using the swaps() function,define two pointers and pass their addresses to the function.
*/
#include <stdio.h>

void swaps(size_t** a, size_t** b) {
    size_t* temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    size_t a = 10;
    size_t b = 20;
    size_t* ptr_a = &a;
    size_t* ptr_b = &b;

    printf("Before swap ptr_a=%p ptr_b=%p \n", (void*)ptr_a, (void*)ptr_b);
    swaps(&ptr_a, &ptr_b);
    printf("After swap ptr_a=%p ptr_b=%p \n", (void*)ptr_a, (void*)ptr_b);

}

