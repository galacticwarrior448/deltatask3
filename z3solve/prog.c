#include <stdio.h>
#define SECRET_VALUE 315525
#define LEN 30

int main() {
    char input[LEN];
    printf("Enter the string: ");
    fgets(input, LEN, stdin);
    int total = 0;

    for (int i = 0; i < LEN; i++) {
        if (input[i] == '\n') break;
        total += (input[i]*input[i] + input[i]*(100 - i) + i + input[i]*7 + ((input[i]|i)&(i+3)));
        total -= (input[i]*input[i]) % (i + 1);
    }

    printf("val: %d\n", total);
    if (total == SECRET_VALUE) {
        printf("flag: you win\n");
    } else {
        printf("nope\n");
    }
}
