#include <stdio.h>

int reverse_digits(int n){
    int reversed = 0;
    while (n > 0){
        int digit = n % 10;
        reversed = reversed * 10 + digit;
        n /= 10;
    }
    return reversed;
}

int main(){
   int n;
    printf("Enter a number: ");
    scanf("%d", &n);
    int reversed = reverse_digits(n);
    printf("Reversed number is: %d\n",reversed);
}
