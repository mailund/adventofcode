#include <stdio.h>

#define N 10
char buf[N];

#define NO_SEATS (1 << N)
int seats[NO_SEATS]; // zero initialised

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
  while (scanf("%s\n", buf) == 1) {
    seats[encode(buf, buf + 10)] = 1;
  }
  for (int i = 1; i < NO_SEATS - 1; i++) {
    if (seats[i - 1] == 1 && seats[i] == 0 && seats[i + 1] == 1) {
      printf("%d\n", i);
      return 0;
    }
  }
  return 0;
}
