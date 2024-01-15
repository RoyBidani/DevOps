#include <string.h>
#include <stdio.h>

void myfunction(int rows, int cols, int matrix[rows][cols], int result[]){
    for(int i = 0; i < rows; i++){
        int sumrow = 0; 
        for(int j = 0; j < cols; j++){
            sumrow += matrix[i][j];
	     }
	 result[i] = sumrow;
	 }
}


int main()
{
    
    int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    int rows = 3;
    int cols = 3;
    int result[3];
    
    myfunction(rows,cols,matrix,result);
    
    for(int i = 0; i < rows; i++){
        printf("sum of row %d: %d\n", i, result[i]);
        }
}


