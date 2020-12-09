section .text
global _asm_test
extern foo

_asm_test:
    xor rax, rax
    xor rax, rax
    here:
    mov byte[rel here], byte 0xc3
    mov byte[rel here], byte 0xc3
    mov byte[rel here], byte 0xc3
    mov byte[rel here], byte 0xc3
    mov byte[rel 34], byte 0x12
    mov byte[rel 0], byte 0x12
    mov rax, 2
    sub rax, qword 42000000
    jmp here
    jmp foo
    mov byte[rel 34], byte 0x12
    xor rax, rax
    ret
