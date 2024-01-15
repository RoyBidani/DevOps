#include <stdio.h>

int power_of_10(int n) {
    int result = 1;
    int i;
    for (i = 0; i < n; i++) {
        result *= 10;
    }
    return result;
}

int main() {
    int n;
    printf("Enter an integer: ");
    scanf("%d", &n);
    int result = power_of_10(n);
    printf("10^%d = %d\n", n, result);
}
