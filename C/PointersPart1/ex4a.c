#include <stdio.h>

void swaps(size_t* a, size_t* b){
    *a = *a + *b ;
    *b = *a - *b ;
    *a = *a - *b ;
}

int main(){
    size_t a;
    size_t b;
    printf("Enter first number: ");
    scanf("%ld", &a);
    printf("Enter second number: ");
    scanf("%ld", &b);
    printf("Before swap a=%ld b=%ld \n",a,b);
    swaps(&a,&b);
    printf("After swap a=%ld b=%ld \n",a,b);
    return 0;
}
