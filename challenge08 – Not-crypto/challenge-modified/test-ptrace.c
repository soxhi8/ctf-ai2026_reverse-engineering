#include <sys/ptrace.h>
#include <stdio.h>
#include <stdlib.h>

void __attribute__((constructor)) anti_debug() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        printf("Debugger detected!\n");
        exit(1);
    }
}
