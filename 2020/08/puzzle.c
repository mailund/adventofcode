#include <stdio.h>
#include <string.h>

struct command { int inc_instp; int inc_acc; };
struct state   { int instp;     int acc;     };
#define CMD(ii, ia) \
  (struct command){ .inc_instp = (ii), .inc_acc = (ia) }

#define N 1000 // the program is shorter than this...
struct command PROG[N];
char visited[N];

static int parse_asm(void)
{
    int n = 0; char buf[4]; int operand;
    while (scanf("%s %d\n", buf, &operand) == 2) {
        if (strcmp(buf, "nop") == 0)      PROG[n++] = CMD(1, 0);
        else if (strcmp(buf, "acc") == 0) PROG[n++] = CMD(1, operand);
        else /* jmp */                    PROG[n++] = CMD(operand, 0);
    }
    return n;
}

struct res { enum { SUCCESS, FAILURE } status; int res; };
#define SUCC(state) (struct res){ .status = SUCCESS, .res = state.acc }
#define FAIL(state) (struct res){ .status = FAILURE, .res = state.acc }

#define UPD(s, cmd) /* important to upd acc before instp */ \
  do { s.acc += cmd.inc_acc; s.instp += cmd.inc_instp; } while(0)

static struct res run(int n)
{
    struct state state = { .instp = 0, .acc = 0 };
    while (state.instp != n) {
        if (visited[state.instp]) return FAIL(state);
        visited[state.instp] = 1;
        UPD(state, PROG[state.instp]);
    }
    return SUCC(state);
}

int main(void)
{
    struct res res = run(parse_asm());
    switch (res.status) {
        case SUCCESS: printf("SUCCESS: %d\n", res.res); break;
        case FAILURE: printf("FAILURE: %d\n", res.res); break;
    }
    return 0;
}
