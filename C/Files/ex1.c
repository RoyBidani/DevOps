#include<stdio.h>

struct print_me {                           // Structure declaration
  int num;                                 // Member (int variable)
  void (*print_ptr)(int);                 // Member (pointer to function)
};                                       // End the structure with a semicolon

void print(int a)
{
  printf("%d\n",a);
}

int main()
{
  
  struct print_me arr[10];
  for(int i = 0; i < 10 ; i++)
  {
    arr[i].num = i ;
    arr[i].print_ptr = &print;        // Assign the function pointer after the structure declaration
    arr[i].print_ptr(arr[i].num);    // printing the array
  }

}
