#ifndef STACK_H
#define STACK_H
#include <stdio.h>

typedef struct
{
    int *head; // a list of int
    int top; // the index of the last int that was pushed

} Stack;


Stack* create(); // create the stack with malloc and return pointer to it

int destroy(Stack* mystack); // free the struct, return 1/0 depands on free()

int pop(Stack* mystack); // remove variable, return top by value and remove it from the stack

int push(Stack* mystack, int element); // add varaible

int peek(Stack* mystack); // return top by value without removing it

int size(Stack* mystack); // count the elements

int isEmpty(Stack* mystack);

int capacity(Stack* mystack); // check the overall size of the stack

#endif 
