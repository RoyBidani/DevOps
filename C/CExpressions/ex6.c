#include <stdio.h>

void swaps(int* a, int* b){
    *a = *a + *b ;
    *b = *a - *b ;
    *a = *a - *b ;
}

int main(){
    int a;
    int b;
    printf("Enter first number: ");
    scanf("%d", &a);
    printf("Enter second number: ");
    scanf("%d", &b);
    printf("Before swap a=%d b=%d \n",a,b);
    swaps(&a,&b);
    printf("After swap a=%d b=%d \n",a,b);
    return 0;
}

