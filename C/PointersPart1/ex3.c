#include <stdio.h>
#include <stdlib.h>

int main()
{

static int s_i = 7;
int i = 7;
int *ptr = &i;
int *ptr2 = (int *)malloc(sizeof(int));

if(ptr){
    int **ptr3 = &ptr;
    printf("ptr3: %p \n", ptr3);
}

free(ptr2);    

printf("s_i: %p\ni: %p\nptr: %p\nptr2: %p\n", &s_i, &i, ptr, ptr2);

}
