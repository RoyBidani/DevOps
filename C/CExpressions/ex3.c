#include <stdio.h>

int main() {
    char str[] = "\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64\x21"; // hex codes for "Hello World!"
    printf("%s\n", str); // print the string
    return 0;
}
