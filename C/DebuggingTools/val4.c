#include <stdio.h>
#include <stdlib.h>

int main() {
    int a;
   int* ptr = malloc(sizeof(int));  
    *ptr = 10;  

   
    free(ptr);
    return 0;
}
