#include <stdio.h>
#include <stdlib.h>
#include "stack.h"



Stack* create(){ // create the stack with malloc and return pointer to it
  Stack* stack = (Stack*)malloc(sizeof(Stack));	// dynamically allocates memory for a new Stack object
  stack->head = NULL;	// initializes to point NULL
  stack->top = -1;	// sempty stack
  return stack;
}

int destroy(Stack* mystack){ // free the struct, return 1/0 depands on free()
  if(mystack == NULL || mystack->top == -1){
    return 1;
  }
  free(mystack->head);	// frees the memory allocated for the Stack array
  free(mystack);	// // frees the memory allocated for the Stack structure
  return 0;
}

int pop(Stack* mystack){ // remove variable, return top by value and remove it from the stack
  if(mystack == NULL || mystack->top == -1){
    return 1;
  }
  int topEl = mystack->head[mystack->top];	// gets the top element on stack
  mystack->top--;	// decrements the pointer to top beacuse we pop element
  return topEl;
}

int push(Stack* mystack, int element) { 	// add varaible
  if (mystack == NULL || mystack->top + 1 >= 100) { 	
    return 1;
  }
  mystack->top++;	// incremetns the value of the head pointer
  mystack->head = (int*)realloc(mystack->head, (mystack->top + 1) * sizeof(int)); 	// resize the array 
  mystack->head[mystack->top] = element;	// assigns the new element to top of stack (array)
  return 0;
}


int peek(Stack* mystack){ // return top by value without removing it
  if(mystack == NULL || mystack->top == -1){
    return 1;
  }
  return mystack->head[mystack->top];  	// returning the value of the top element in stack
}

int size(Stack* mystack){ // count the elements
  if(mystack == NULL || mystack->top == -1){
    return 1;
  }
  return mystack->top + 1;
}

int isEmpty(Stack* mystack){
  if(mystack == NULL || mystack->top == -1){
    return 0;
  }
  return 1;  

}

int capacity(Stack* mystack){ // check the overall size of the stack
    return 100; 
}


int main(){
  Stack* mystack = create();
  push(mystack,10);
  push(mystack,20);
  push(mystack,30);
  push(mystack,40);
  
  
  
  printf("Top element: %d\n", peek(mystack));
  printf("Size of stack: %d\n", size(mystack));
  
  
  

}

