#include <stdio.h>
#include <stdlib.h>

void copyArray(int* arr1, int* arr2, int size)
{
    int i; 
    for(int i = 0; i < size; i++){
        arr2[i] = arr1[i];
        }

}

int main()
{
    int arr1[] = {1,2,3,4,5,6,7,8,9,10};
    int size = sizeof(arr1) / sizeof(arr1[0]);
    int arr2[size];
    
    int i;
    copyArray(arr1, arr2, size);
    printf("The 2 arrays after copy: \n\n");
    
    for(i=0;i<size;i++){
        printf("argue number %d: \n array1: %d	array2: %d \n", i,arr1[i],arr2[i]);
        printf("\n");
        }
    
    
   
}
