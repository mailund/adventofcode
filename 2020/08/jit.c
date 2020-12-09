#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>

// There is about 1k instructions and I need 16 bytes per
// instruction, so I allocate four pages for the jit'ed code
#define PAGESIZE 4096
struct jit_buf {
    unsigned char buf[4 * PAGESIZE - sizeof(int)];
    int next_inst;
};
struct jit_buf *alloc_jit_buf(void)
{
    int protection = PROT_WRITE | PROT_EXEC;
    int flags = MAP_ANONYMOUS | MAP_PRIVATE;
    struct jit_buf *buf = mmap(0, 4 * PAGESIZE, protection, flags, -1, 0);
    if (!buf) return 0;
    buf->next_inst = 0;
    return buf;
}

// General code emission functions
static inline
void emit_byte(struct jit_buf *buf, char byte)
{ buf->buf[buf->next_inst++] = byte; }

static inline
void emit_int(struct jit_buf *buf, uint32_t n)
{ emit_byte(buf, n & 0xff); emit_byte(buf, (n >> 8) & 0xff);
  emit_byte(buf, (n >> 16) & 0xff); emit_byte(buf, (n >> 24) & 0xff); 
}

// This is just to make addressing easier. We can use the same
// number of bytes for each instruction, and that way have a simple
// jmp instruction. Instructions start at multiples of 16
static inline
void pad(struct jit_buf *buf, int bytes)
{ for (int i = 0; i < bytes; i++) emit_byte(buf, 0x90); /* nop */ }

// For setting up the JIT function -- we need to start with acc = 0
static void zero_acc(struct jit_buf *buf)
{   // xor rax, rax
    emit_byte(buf, 0x48); emit_byte(buf, 0x31); emit_byte(buf, 0xc0);
}
// If we reach the end of the program, use this to return
static void ret(struct jit_buf *buf)
{
    emit_byte(buf, 0xc3); 
}

// Here we write some self-modifying code that
// will return from the function if we ever return
// to this point. The instruction is
// mov byte[rip - 7], byte 0xc3
// where 0xc3 is the opcode for ret.
static void return_guard(struct jit_buf *buf)
{
    emit_byte(buf, 0xc6); emit_byte(buf, 0x05); // mov a byte
            emit_int(buf, -7);                  // write to 7 bytes back
            emit_byte(buf, 0xc3);               // the `ret` opcode
}

static void nop(struct jit_buf *buf)
{
    return_guard(buf);
    pad(buf, 9);
}

static void acc(struct jit_buf *buf, int n)
{
    return_guard(buf);
    // add rax, dword <n>
    emit_byte(buf, 0x48); emit_byte(buf, 0x05); emit_int(buf, n);
    pad(buf, 3);
}

static void jmp(struct jit_buf *buf, int n)
{
    return_guard(buf);
    // jmp <n> -- adjust for the address of this instruction
    //               and then 16-step jumps for steps in our VM instructions
    emit_byte(buf, 0xe9);
    if (n > 0) emit_int(buf, 16 * (n - 1) + 4);
    else       emit_int(buf, 16 * n - 12);
    pad(buf, 4);
}

static int (*parse_asm(void))(void)
{
    struct jit_buf *buf = alloc_jit_buf();
    zero_acc(buf); // setup accumulator in generated function
    char opcode[4]; int operand;
    while (scanf("%s %d\n", opcode, &operand) == 2) {
        if (strcmp(opcode, "nop") == 0)      /* emit => */ nop(buf);
        else if (strcmp(opcode, "acc") == 0) /* emit => */ acc(buf, operand);
        else /* jmp */                       /* emit => */ jmp(buf, operand);
    }
    ret(buf); // add a return if we reach the end of the program
    return (int (*)(void))buf;
}


int main(void)
{
    int (*prog)(void) = parse_asm();
    printf("%d\n", prog());
    return 0;
}
