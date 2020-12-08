#include <stdio.h>
#include <string.h>
#include <stdint.h>

typedef uint32_t inst;
typedef uint32_t state;

#define ACC_MASK       ((1 << 16) - 1)
#define INSTP(x)       (x >> 16)
#define ACC(x)         (x & ACC_MASK)
#define ADD_INSTP(x,y) ((INSTP(x) + INSTP(y)) << 16)
#define ADD_ACC(x,y)   ((ACC(x) + ACC(y)) & ACC_MASK)
#define ADD(x,y)       (ADD_INSTP(x,y) | ADD_ACC(x,y))

#define CMD(inc_instp, inc_acc) ((inc_instp << 16) | (inc_acc & ACC_MASK))

#define N 1000 // the program is shorter than this...
inst PROG[N];
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
#define SUCC(state) (struct res){ .status = SUCCESS, .res = ACC(state) }
#define FAIL(state) (struct res){ .status = FAILURE, .res = ACC(state) }

#define UPD(s, cmd) /* important to upd acc before instp */ \
  do { s.acc += cmd.inc_acc; s.instp += cmd.inc_instp; } while(0)

static struct res run(int n)
{
    state s = 0; int instp = 0;
    while (instp != n) {
        printf("<%d %d>\n", INSTP(s), ACC(s));
        if (visited[instp]) return FAIL(s); visited[instp] = 1;
        s = ADD(s, PROG[instp]); instp = INSTP(s);
    }
    return SUCC(s);
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
