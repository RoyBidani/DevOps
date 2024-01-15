#include <string.h>
#include <stdio.h>
#include <assert.h>

size_t StrLen(const char* str) {
    assert(str != NULL);
    size_t len = 0;
    while (*str != '\0') {
        ++len;
        ++str;
    }
    return len;
}

int StrCmp(const char* str1, const char* str2) {
    assert(str1 != NULL && str2 != NULL);
    while (*str1 == *str2) {
        if (*str1 == '\0') {
            return 0;
        }
        ++str1;
        ++str2;
    }
    return (*str1 < *str2) ? -1 : 1;
}

int main()
{
    char str1[100];
    char str2[100];
    size_t len1 = 0;
    size_t len2 = 0;
    printf("Enter your first string: \n");
    scanf("%s", str1);
    len1 = StrLen(str1);
    printf("Enter your second string: \n");
    scanf("%s", str2);
    len2 = StrLen(str2);
    
    printf("Your first String length: %ld \n",len1);
    printf("Your second String length: %ld \n",len2);
    
   (StrCmp(str1, str2) == 0) ? printf("Strings are equal! \n") : printf("Strings are not equal! \n");

    

}
