#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char lastInput[100] = ""; 

enum Result{
  SUCCESS,
  FAILURE
};

struct Special{
  char name[100];						// member string
  int (*cmpr)(char[]);						// member pointer to function
  enum Result (*func)(char *);						// member pointer to function
};


enum Result removeFile(char *file_name){
  FILE *file = fopen(file_name, "r+");       			// open the file in read & write mode 
  if(remove(file_name) == 0){
    printf("file deleted successfuly\n");
    return SUCCESS;
  }else {
    printf("cant delete this file\n");
    return FAILURE;
  }
 
}

enum Result countFile(char *file_name){
  FILE *file = fopen(file_name, "r+");       			// open the file in read & write mode 
  int count = 0;             		            		// line counter
  int ch;                    		          		 // char indicator
  fseek(file, 0, SEEK_SET);  			 		 // set file indicator to the beginning of the file.
  while ((ch = fgetc(file)) != EOF) {   			 // running on every letter in the file
    if (ch == '\n') {
      count++;           		      			 // when we get to the end of line, increment the count value by 1
    }
  }
  printf("Number of lines: %d\n", count); 
  if(count > 0){
    return SUCCESS;
  }else{
    return FAILURE;
  }
}


enum Result exitFile(char *file_name){
  return SUCCESS;
  exit(0);                					// exit the program
}


enum Result writeFile(char *file_name) {
  char input[100];
  FILE *file = fopen(file_name, "r+");       			// open the file in read & write mode
  fseek(file, 0, SEEK_SET);         				 // set file position to the beginning of the file.
  fputs(lastInput, file);  					// write the string from last inpur to the file 
  
  fclose(file);  // Close the file
  if(lastInput != NULL){
    return SUCCESS;
  }else {
    return FAILURE;  
  }
}


int cmpr_remove(char string[]){
  if(strcmp(string, "-remove") == 0){
    return 1;
  } 
  else {
    return 0;
  }
}

int cmpr_count(char string[] ){
  if(strcmp(string, "-count") == 0){
    return 1;
  } 
  else {
    return 0;
  }
}


int cmpr_exit(char string[]){
  if(strcmp(string, "-exit") == 0){
    return 1;
  } 
  else {
    return 0;
  }
}

int cmpr_write(char string[]){
  if(string[0] == '<'){
    return 1;
  } 
  else {
    return 0;
  }
}


int main()
{
    struct Special arr[4];
    strcpy(arr[0].name, "-remove");   // Assign a value to the name member of the first command
    strcpy(arr[1].name, "-count");  // Assign a value to the name member of the second command
    strcpy(arr[2].name, "-exit");   // Assign a value to the name member of the third command
    strcpy(arr[3].name, "<");  // Assign a value to the name member of the fourth command 
 
   
    arr[0].func = &removeFile;  // Assign the relevant function pointer
    arr[1].func = &countFile;
    arr[2].func = &exitFile;
    arr[3].func = &writeFile;
    
    arr[0].cmpr = &cmpr_remove;  // Assign the relevant compare function pointer
    arr[1].cmpr = &cmpr_count;
    arr[2].cmpr = &cmpr_exit;
    arr[3].cmpr = &cmpr_write;

    
    char file_name[100];
    char string[100];

    printf("Enter a file name: ");
    scanf("%s", file_name);
    getchar(); 					// Consume the newline character from the input buffer
    
    printf("Enter your command: ");
    fgets(string, sizeof(string), stdin);
    string[strcspn(string, "\n")] = '\0';  // Remove the newline character from fgets

    strcpy(lastInput, &string[1]);  // Store the last input (excluding the '<' character) in the lastInput variable

    
    for(int i = 0; i < 4 ; i ++){
      if(arr[i].cmpr(string) == 1){
        if (arr[i].func(file_name) == SUCCESS) {
                printf("Function executed successfully.\n");
            } else {
                printf("Function execution failed.\n");
            }
      }
    }
  }

