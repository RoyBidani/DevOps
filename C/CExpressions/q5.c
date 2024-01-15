#include <stdio.h>

int main()
{
    int x = 20;
    int y = 35;
    x = y++ + x++;
    y = ++y + ++x;
    printf("%d %d \n",x ,y);
}
