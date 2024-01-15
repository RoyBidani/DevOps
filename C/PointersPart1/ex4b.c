#include <stdio.h>
#include <stdlib.h>

void swaps(size_t** a, size_t** b){
    size_t* temp = *a ;
    *a = *b ;
    *b = temp;
}

int main(){
    size_t* a = (size_t*) malloc(sizeof(size_t));
    size_t* b = (size_t*) malloc(sizeof(size_t));
    printf("Enter first number: ");
    scanf("%zu", a);
    printf("Enter second number: ");
    scanf("%zu", b);
    printf("Before swap a=%zu b=%zu \n",*a,*b);
    swaps(&a,&b);
    printf("After swap a=%zu b=%zu \n",*a,*b);
    
}
