#include <stdio.h>

extern void __assert_fail(const char *, const char *, unsigned int, const char *) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__noreturn__));

void reach_error() {
    __assert_fail("0", "generated.c", 1, "reach_error");
}
int main() {
    int trigger = 0;
    trigger += 1;
    trigger += 2;
    trigger += 3;
    trigger += 4;
    trigger += 5;
    trigger += 6;
    trigger += 7;
    trigger += 8;
    trigger += 9;
    trigger += 10;
    if (trigger == 55) {
        reach_error();
    }
}
