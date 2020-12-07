#include <stdio.h>

#define N (26 + 2)
char buf[N];

int handle_group(int *un, int *inter)
{
    *un = 0; *inter = ~0;
    while (fgets(buf, N, stdin)) {
        if (buf[0] == '\n') return *un; // zero if we read nothing
        int ans = 0;
        for (char *x = buf; *x != '\n'; x++) ans |= (1 << (*x - 'a'));
        *un |= ans; *inter &= ans;
    }
}

#define set_size(set) __builtin_popcount(set)
int main(void)
{
    int un, inter, count_un = 0, count_inter = 0;
    while (handle_group(&un, &inter)) {
        count_un += set_size(un);
        count_inter += set_size(inter);
    };
    printf("%d %d\n", count_un, count_inter);
    return 0;
}