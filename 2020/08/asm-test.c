#include <stdio.h>

extern int asm_test(void);

int main(void)
{
    printf("%d\n", asm_test());
    return 0;
}