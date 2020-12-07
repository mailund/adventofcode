#include <stdio.h>

#define N 10
char buf[N];

static int encode(char *start, char *end)
{
  int val = 0;
  for (; start != end; start++) {
    val <<= 1;
    if (*start == 'B' || *start == 'R') val |= 1;
  }
  return val;
}

int main(void)
{
  int max = 0;
  while (scanf("%s\n", buf) == 1) {
    int pass = encode(buf, buf + 10);
    if (pass > max) max = pass;
  }
  printf("%d\n", max);
  return 0;
}
