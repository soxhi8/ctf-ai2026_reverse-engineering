#include <stdio.h>
#include <stdlib.h>

/*
This is not the challenge, just a template to answer the questions.
To get the flag, answer all the questions. 
There are no bugs in the quiz.
There are 0xD questions in total.

*/

void win(){
        system("cat flag.txt");
}

void vuln(){
        char buffer[0x15] = {0};
        fprintf(stdout, "\nEnter payload: ");
        fgets(buffer, 0x90, stdin);
}

void main(){
        vuln();
}

/*
====================================================================
DEBUG LOG OUTPUT
====================================================================
Buffer Analysis:
- Allocated buffer size: 32 bytes (0x20)
- Bytes read in fgets: 256 bytes (0x100)
- Overflow amount: 224 bytes (0xE0)

Vulnerability Assessment:
- Vulnerability class: Format String Vulnerability
- Vulnerable function: printf
- Unused functions identified: target_function

Exploit Mitigation Status:
- Protections: Stack Canary enabled
- Bypass technique: Bruteforce
====================================================================
*/
