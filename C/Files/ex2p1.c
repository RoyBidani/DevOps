#include <stdio.h>

int main()
{
  char file_name[100];
  char string[100];
  
  printf("Enter a file name: ");
  scanf("%s", file_name);
  
  FILE *file = fopen(file_name, "a");  	      // open the file in append mode
  
  printf("Enter a string: ");
  
  getchar();                              // consume the newline character left in the input buffer
  fgets(string, sizeof(string), stdin);  // read the complete line
  fprintf(file, "%s",string);	        // append string to end of file
  
  fclose(file);			      // close the file
}
